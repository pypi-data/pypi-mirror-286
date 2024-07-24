
import unittest
import requests
from mantlebio.core.session.helpers import MantleSessionResponse
from mantlebio.exceptions import MantleApiError, MantleAuthenticationError, MantleClientError, MantleResourceNotFoundError

class TestMantleSessionResponse(unittest.TestCase):

    def test_raise_for_status_with_successful_response(self):
        response = requests.Response()
        response.status_code = 200
        mantle_response = MantleSessionResponse(response)

        # No exception should be raised
        mantle_response.raise_for_status()

    def test_raise_for_status_with_authentication_error(self):
        response = requests.Response()
        response.status_code = 401
        mantle_response = MantleSessionResponse(response)

        with self.assertRaises(MantleAuthenticationError):
            mantle_response.raise_for_status()

    def test_raise_for_status_with_resource_not_found_error(self):
        response = requests.Response()
        response.status_code = 404
        mantle_response = MantleSessionResponse(response)

        with self.assertRaises(MantleResourceNotFoundError):
            mantle_response.raise_for_status()

    def test_raise_for_status_with_api_error(self):
        response = requests.Response()
        response.status_code = 500
        response._content = b"API error response"
        mantle_response = MantleSessionResponse(response)

        with self.assertRaises(MantleApiError):
            mantle_response.raise_for_status()

    def test_raise_for_status_with_client_error(self):
        response = requests.Response()
        response.status_code = 400
        response._content = b"Client error response"
        mantle_response = MantleSessionResponse(response)

        with self.assertRaises(MantleClientError):
            mantle_response.raise_for_status()

if __name__ == '__main__':
    unittest.main()