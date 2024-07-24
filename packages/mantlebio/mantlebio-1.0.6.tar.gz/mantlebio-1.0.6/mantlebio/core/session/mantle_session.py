

import os
import time
from typing import Any, List, Optional, Union
from mantlebio.core.auth.creds import AuthMethod
from mantlebio.core.auth.mantle_auth import MantleAuth
from mantlebio.core.constants import MANTLE_API_MAP, MANTLE_PROD_API
from mantlebio.core.session.helpers import MantleSessionResponse
from mantlebio.exceptions import MantleAuthenticationError, MantleConfigurationWarning, MantleInvalidParameterError, MantleMissingParameterError, MantleRetriesExceededError

from abc import abstractmethod

from mantlebio.core.session.helpers import MantleSessionResponse
import requests
from google.protobuf.message import Message

from mantlebio.helpers.decorators import deprecated


class _ISession(requests.Session):
    """
    Abstract base class for session objects. Wraps the requests.Session object.

    Attributes:
        tenant_id (str): The ID of the current tenant.
        env (str): The environment of the session.

    Methods:
        authenticate(tenant_id: Optional[str] = None, env: str = 'PROD'): Authenticates the session.
        sign_out(): Signs out the session.
        make_request(method: str, url: str, json: Optional[dict] = None, data: Optional[Message] = None, params: Optional[dict] = None) -> MantleSessionResponse: Makes a request using the session.
        set_verify(verify: bool): Sets the verification flag for the session.
        validate_tenant(tenant_selection: str, all_valid_tenants: List[str]): Validates the selected tenant.
        _raise_for_status(response: requests.Response): Raises an exception for the response status.
        get_tenant_id(): Returns the ID of the current tenant.
    """
    @abstractmethod
    def authenticate(self, tenant_id: Optional[str] = None, env: str = 'PROD'):
        pass

    @abstractmethod
    def sign_out(self):
        pass

    @abstractmethod
    def make_request(self, method: str, url: str, json: Optional[dict] = None, data: Optional[Message] = None, params: Optional[dict] = None) -> MantleSessionResponse:
        pass

    @abstractmethod
    def set_verify(self, verify: bool):
        pass

    @abstractmethod
    def validate_tenant(self, tenant_selection: str, all_valid_tenants: List[str]):
        pass

    @abstractmethod
    def _raise_for_status(self, response: requests.Response):
        pass

    @abstractmethod
    def get_tenant_id(self):
        pass


class MantleSession(_ISession):
    """MantleSession object for making requests to the Mantle API"""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super(MantleSession, self).__init__(*args, **kwargs)
        self.headers.update(
            {
                'Content-Type': 'application/protobuf',
            }
        )
        self._max_retries = 2

    # TODO remove the parent_client parameter in version 2.0.0
    def authenticate(self, tenant_id: Optional[str] = None, env: str = 'PROD', creds: Union[AuthMethod, None] = None) -> None:
        """Authenticate the session object

        Args:
          env (str, optional): Environment to authenticate against. Defaults to 'PROD'.
        """
        self.env = env

        self.host = MANTLE_API_MAP.get(env.upper())

        if not self.host:
            self.host = MANTLE_PROD_API
            raise MantleConfigurationWarning(
                f"No host found for environment {env} setting to {MANTLE_PROD_API}")

        self.mantle_auth: MantleAuth = MantleAuth(
            mantle_api=self.host, creds=creds)
        login_resp = self.mantle_auth.authenticate()

        if not login_resp or not login_resp.ok:
            raise MantleAuthenticationError("Authentication failed")

        if not tenant_id:
            tenant_id = ""

        self.validate_tenant(tenant_id, login_resp.json().get("tenants"))
        self.headers.update(
            {
                'Authorization': f"Bearer {self.mantle_auth.get_token()}"
            }
        )

    def sign_out(self):
        """Sign out of the session object"""
        self.mantle_auth.sign_out()
        self.host = None

    def get_tenant_id(self):
        return self.tenant_id

    # TODO (pmoradi)
    # unit test on retry
    def make_request(self, method: str, url: str, json: Optional[dict] = None, data: Optional[Message] = None, params: Optional[dict] = None, headers: Optional[dict] = None) -> MantleSessionResponse:
        """
        Make a request to the Mantle API

        Args:
            method (str): HTTP method
            url (str): URL to make the request to
            json (dict, optional): JSON data to send in the request
            data (Message, optional): Protobuf data to send in the request
            params (dict, optional): Query parameters to send in the request

        Returns:
            requests.Response: Response object

        Raises:
            AuthenticationError: If the session is not authenticated
            ResourceNotFoundError: If the resource is not found
            MantleApiError: If the API returns a 5xx status code
            RetriesExceededError: If the maximum number of retries is exceeded
        """
        req_data = None
        if self.host is None:
            raise Exception("Session not authenticated")
        if data:
            req_data = data.SerializeToString()

        full_url = f"{self.host}/{self.tenant_id}{url}"
        backoff_factor = 1  # Initial backoff factor, adjust as needed

        for attempt in range(self._max_retries):
            response = MantleSessionResponse(self.request(
                method, full_url, json=json, params=params, data=req_data, headers=headers))
            if response.status_code < 300:
                return response
            elif response.status_code in [500, 502, 503, 504]:
                print(
                    f"Transient error received ({response.status_code}), retrying in {backoff_factor} seconds...")
                time.sleep(backoff_factor)
                backoff_factor *= 2  # Exponential backoff
                continue
            elif response.status_code == 401 and attempt == 0:
                print("401 Unauthorized received, attempting to re-authenticate.")
                try:
                    self.authenticate(self.tenant_id, self.env)
                    # re-try the request
                    continue
                except Exception as e:
                    raise MantleAuthenticationError(
                        "Failed to re-authenticate") from e
            return response

        raise MantleRetriesExceededError("Maximum retries exceeded")

    def set_verify(self, verify: bool):
        """Sets the verify boolean of a request.Session object

        Args:
          verify (bool): Boolean for validating certificates
        """
        self.verify = verify

    def validate_tenant(self, tenant_selection: str, all_valid_tenants: List[str]):
        """
        Validate the tenant ID

        Args:
            tenant_selection (str): Tenant ID
            all_valid_tenants (List[str]): List of valid tenant IDs

        Raises:
            InvalidParameterError: If the tenant ID is invalid
            MissingParameterError: If the tenant ID is missing and there are multiple valid tenants

        """
        if not tenant_selection and len(all_valid_tenants) == 1:
            self.tenant_id = all_valid_tenants[0]
            return
        if tenant_selection and tenant_selection in all_valid_tenants:
            self.tenant_id = tenant_selection
            return
        if tenant_selection and tenant_selection not in all_valid_tenants:
            raise MantleInvalidParameterError(
                f"Invalid tenant ID. User has access to these tenants:"
                f" {all_valid_tenants}"
            )
        if not tenant_selection and os.getenv('MANTLE_TENANT'):
            self.tenant_id = os.getenv('MANTLE_TENANT')
            return
        if not tenant_selection and not os.getenv('MANTLE_TENANT') and len(all_valid_tenants) != 1:
            raise MantleMissingParameterError(
                f"Please provide a tenant. User has access to "
                f" these tenants: {all_valid_tenants}"
            )
