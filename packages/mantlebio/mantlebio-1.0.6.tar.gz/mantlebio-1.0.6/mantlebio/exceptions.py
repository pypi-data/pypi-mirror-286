
# All exceptions should subclass from MantlebioError in this module.
class MantlebioError(Exception):
    """Base class for all Mantlebio errors."""
    pass
    
class MantleAuthenticationError(MantlebioError):
    pass

class MantleConfigurationError(MantlebioError):
    pass

class MantleInvalidParameterError(MantlebioError):
    pass

class MantleMissingParameterError(MantlebioError):
    pass

class MantleClientError(MantlebioError):
    pass

class MantleTypeError(MantlebioError):
    def __init__(self, type ) -> None:
        super().__init__(f"Invalid type {type}")
class StorageUploadError(MantlebioError):
    pass

class MantleResourceNotFoundError(MantlebioError):
    def __init__(self, request_url, response_content):
        super().__init__(f"Resource not found: {request_url} got response: {response_content}")

class MantleRetriesExceededError(MantlebioError):
    def __init__(self, last_exception, msg='Max Retries Exceeded'):
        super().__init__(msg)
        self.last_exception = last_exception

class MantleQueryBuilderError(MantlebioError):
    def __init__(self, msg):
        super().__init__(msg)

class MantleApiError(MantlebioError):
    pass

class MantleProtoError(MantlebioError):
    def __init__(self, content, proto):
        super().__init__(f"Failed to parse response as {proto}. Response: {content}")

class MantleResponseError(MantlebioError):
    pass

class MantleAttributeError(MantlebioError):
    pass

class MantlebioWarning(Warning):
    """
    Warning for Mantle API related issues.
    """
    pass

class MantleConfigurationWarning(MantlebioWarning):
    """
    Warning for Mantle configuration issues.
    """
    pass

class PythonDeprecationWarning(Warning):
    """
    Python version being used is scheduled to become unsupported
    in an future release. See warning for specifics.
    """
    pass
