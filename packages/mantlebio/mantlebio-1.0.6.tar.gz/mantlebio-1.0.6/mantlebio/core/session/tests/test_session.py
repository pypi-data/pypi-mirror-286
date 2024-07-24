import unittest
from unittest.mock import patch, MagicMock
from mantlebio.core.session.mantle_session import MantleSession
from mantlebio.exceptions import MantleResourceNotFoundError
from requests.exceptions import HTTPError

import os

class TestMantleSession(unittest.TestCase):

    def setUp(self):
        os.environ["ENV"] = "unittest"
        self.session = MantleSession()
        self.session.host = 'https://mantle.test.com'
        self.session.env = "unittest"
        self.session.tenant_id = "test_tenant"
    
    @patch.object(MantleSession, 'authenticate')
    @patch('requests.Session.request')
    def test_reauth_on_401_response(self, mock_request, mock_authenticate):
        response_401 = MagicMock()
        response_401.ok = False
        response_401.status_code = 401
        response_401.raise_for_status.side_effect = HTTPError()

        response_200 = MagicMock()
        response_200.ok = True
        response_200.status_code = 200

        # return 401 on first call and 200 on second
        mock_request.side_effect = [response_401,  response_200]

        response = self.session.make_request('GET', '/test')

        mock_authenticate.assert_called_once()
        self.assertEqual(mock_request.call_count, 2)
        self.assertEqual(response.status_code, 200)

    @patch('requests.Session.request')
    def test_no_retry_on_non_transient_response(self, mock_request):
        response_404 = MagicMock()
        response_404.ok = False
        response_404.reason = "Not Found"
        response_404.status_code = 404
        response_404.url = "https://mantle.test.com/test"
        response_404._content = "test_content"
        response_404.raise_for_status.side_effect = MantleResourceNotFoundError("test_url", "test_content")

        mock_request.side_effect = [response_404]

        with self.assertRaises(MantleResourceNotFoundError):
            req = self.session.make_request('GET', '/test')

            if not req.ok:
                req.raise_for_status()

        self.assertEqual(mock_request.call_count, 1)

if __name__ == '__main__':
    unittest.main()