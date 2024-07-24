import unittest
from unittest.mock import patch, MagicMock

from mantlebio.core.auth.mantle_auth import MantleAuth
from mantlebio.core.auth.creds import JwtCredentials
from mantlebio.core.constants import MANTLE_PROD_API


class TestMantleAuth(unittest.TestCase):
    """
    Unit tests for the MantleAuth class.
    """

    def setUp(self):
        self.mantle_auth = MantleAuth()

    def test_init(self):
        auth = MantleAuth()
        self.assertEqual(auth._mantle_api, MANTLE_PROD_API)
        self.assertEqual(auth._access_token, "")
        self.assertIsNone(auth.creds)

    @patch('requests.post')
    def test_authenticate_password_success(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {
                                           "access_token": "test_token"})
        with patch('os.getenv', side_effect=lambda k: {"MANTLE_USER": "test_user", "MANTLE_PASSWORD": "test_password"}.get(k)):
            self.mantle_auth.authenticate()
            self.assertEqual(self.mantle_auth.get_token(), "test_token")

    @patch('requests.post')
    def test_sign_out(self, mock_post):
        self.mantle_auth.sign_out()
        mock_post.assert_called_with(self.mantle_auth._mantle_api + '/signout')

    def test_get_token(self):
        auth = MantleAuth(creds=JwtCredentials("test_token"))
        self.assertEqual(auth.get_token(), "test_token")


if __name__ == '__main__':
    unittest.main()
