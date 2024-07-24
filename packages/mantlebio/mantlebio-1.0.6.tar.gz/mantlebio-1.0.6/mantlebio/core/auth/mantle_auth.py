
from abc import abstractmethod
from getpass import getpass
import os
from typing import Union
from dotenv import load_dotenv
from mantlebio.core.constants import MANTLE_PROD_API
from mantlebio.helpers.decorators import deprecated
import requests
import time
import random
from mantlebio.exceptions import MantleAuthenticationError, MantleRetriesExceededError
from mantlebio.core.auth.creds import AuthMethod, PasswordCredentials


class _IAuth:
    """Abstract class for authenticating with Supabase"""

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def sign_out(self):
        pass

    @abstractmethod
    def get_token(self):
        pass


class MantleAuth(_IAuth):
    """MantleAuth object for authenticating with Supabase"""

    def __init__(self, creds: Union[AuthMethod, None] = None, mantle_api: str = MANTLE_PROD_API) -> None:
        load_dotenv()
        self._access_token = ""
        self._mantle_api = mantle_api
        self.creds = creds

    def authenticate(self, mantle_api: Union[str, None] = None):
        """Authenticate the session object

        Returns:
          dict: response from the API
        """
        if not self.creds:
            self.creds = PasswordCredentials()

        if not mantle_api:
            mantle_api = self._mantle_api  # use default mantle_api
        return self.creds.authenticate(mantle_api=mantle_api)

    def sign_out(self):
        # make call to mantle API
        requests.post(
            self._mantle_api + '/signout'
        )
        pass

    def get_token(self):
        if not self.creds:
            raise MantleAuthenticationError("No credentials provided")
        return self.creds.get_token()
