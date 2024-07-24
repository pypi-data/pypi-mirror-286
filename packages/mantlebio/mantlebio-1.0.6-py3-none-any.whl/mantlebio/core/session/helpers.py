
from mantlebio.exceptions import MantleApiError, MantleAuthenticationError, MantleClientError, MantleResourceNotFoundError
import requests

class MantleSessionResponse(requests.Response):
    def __init__(self, response: requests.Response):
        # Copy necessary attributes from the passed response object
        self.__dict__.update(response.__dict__)
        
    def raise_for_status(self):
        try:
            super(MantleSessionResponse, self).raise_for_status()
        except requests.exceptions.HTTPError as e:
            if self.status_code == 401:
                raise MantleAuthenticationError("Authentication failed") from e
            elif self.status_code == 404:
                raise MantleResourceNotFoundError(self.url, self.content) from e
            elif self.status_code >= 500:
                raise MantleApiError(f"API returned status code {self.status_code} with response: {self.content}") from e
            elif self.status_code >= 400:
                raise MantleClientError(f"API returned status code {self.status_code} with response: {self.content}") from e
            else:
                # If none of the custom conditions are met, re-raise the original exception
                raise e

