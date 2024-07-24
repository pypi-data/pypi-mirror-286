import os
from typing import Optional
from mantlebio.core.session.helpers import MantleSessionResponse
from mantlebio.core.session.mantle_session import _ISession
from requests import Response


def custom_isfile(mock_file_path):
    '''
    Custom isfile function to mock os.path.isfile

    Args:
        mock_file_path: path to file to mock

    Returns:
        True if path is equal to mock_file_path, generic isfile otherwise
    '''
    def fn(path):
        if path == mock_file_path:
            return True
        else:
            return os.path.isfile(path)
    return fn

def create_test_reponse(status_code: int, content: Optional[bytes] = None, url: Optional[str] = None)-> MantleSessionResponse:
    '''
    Create a test response object

    Args:
        status_code: status code of the response
        content: content of the response

    Returns:
        Response object
    '''
    response = Response()
    response.status_code = status_code
    response._content = content
    response.url = url or ""

    return MantleSessionResponse(response)

def create_large_test_file(filename, size_mb=205):
    # 1 MB = 1,048,576 bytes
    size_in_bytes = size_mb * 1048576
    with open(filename, 'wb') as f:
        f.write(b'0' * size_in_bytes)

def create_test_session(authenticate_fns=[], set_verify_fns=[], make_request_fns=[], validate_tenant_fns=[], sign_out_fns=[])-> _ISession:
    class TestSession(_ISession):
        def __init__(self):
            self.tenant_id = "test"
            self.authenticate_calls = 0
            self.set_verify_calls = 0
            self.make_request_calls = 0
            self.validate_tenant_calls = 0
            self.sign_out_calls = 0


        def authenticate(self, tenant_id: str, env: str):
            if not authenticate_fns or len(authenticate_fns) <= self.authenticate_calls:
                return

            self.authenticate_calls += 1
            return authenticate_fns[self.authenticate_calls-1]()
        
        def set_verify(self, verify: bool):
            if not set_verify_fns or len(set_verify_fns) <= self.set_verify_calls:
                return

            self.set_verify_calls += 1
            return set_verify_fns[self.set_verify_calls-1]()
        
        def make_request(self, method: str, url: str, json: dict = {}, data = {}, params: dict = {}):
            if not make_request_fns or len(make_request_fns) <= self.make_request_calls:
                return

            self.make_request_calls += 1
            return make_request_fns[self.make_request_calls-1]()
        
        def validate_tenant(self, tenant_selection: str, all_valid_tenants: list):
            if not validate_tenant_fns or len(validate_tenant_fns) <= self.validate_tenant_calls:
                return

            self.validate_tenant_calls += 1
            return validate_tenant_fns[self.validate_tenant_calls-1]()

        def sign_out(self):
            if not sign_out_fns or len(sign_out_fns) <= self.sign_out_calls:
                return

            self.sign_out_calls += 1
            return sign_out_fns[self.sign_out_calls-1]()
        
    return TestSession()