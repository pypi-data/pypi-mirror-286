from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PostIntegrationRequest(_message.Message):
    __slots__ = ("github",)
    GITHUB_FIELD_NUMBER: _ClassVar[int]
    github: PostGithubIntegration
    def __init__(self, github: _Optional[_Union[PostGithubIntegration, _Mapping]] = ...) -> None: ...

class PostGithubIntegration(_message.Message):
    __slots__ = ("name", "repo", "token")
    NAME_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    name: str
    repo: str
    token: str
    def __init__(self, name: _Optional[str] = ..., repo: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class GithubIntegration(_message.Message):
    __slots__ = ("id", "name", "repo")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    repo: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., repo: _Optional[str] = ...) -> None: ...

class GithubIntegrationsResponse(_message.Message):
    __slots__ = ("repos",)
    REPOS_FIELD_NUMBER: _ClassVar[int]
    repos: _containers.RepeatedCompositeFieldContainer[GithubIntegration]
    def __init__(self, repos: _Optional[_Iterable[_Union[GithubIntegration, _Mapping]]] = ...) -> None: ...

class BucketConfig(_message.Message):
    __slots__ = ("bucket", "region", "endpoint_url", "integration")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_URL_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    region: str
    endpoint_url: str
    integration: Integration
    def __init__(self, bucket: _Optional[str] = ..., region: _Optional[str] = ..., endpoint_url: _Optional[str] = ..., integration: _Optional[_Union[Integration, _Mapping]] = ...) -> None: ...

class Integration(_message.Message):
    __slots__ = ("id", "integration_id", "access_token")
    ID_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    id: str
    integration_id: str
    access_token: str
    def __init__(self, id: _Optional[str] = ..., integration_id: _Optional[str] = ..., access_token: _Optional[str] = ...) -> None: ...

class IntegrationsResponse(_message.Message):
    __slots__ = ("integrations",)
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[Integration]
    def __init__(self, integrations: _Optional[_Iterable[_Union[Integration, _Mapping]]] = ...) -> None: ...

class StorageConfiguration(_message.Message):
    __slots__ = ("upload_bucket", "endpoint_url", "region", "upload_prefix", "integration", "buckets")
    UPLOAD_BUCKET_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_URL_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_PREFIX_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    upload_bucket: str
    endpoint_url: str
    region: str
    upload_prefix: str
    integration: Integration
    buckets: _containers.RepeatedCompositeFieldContainer[BucketConfig]
    def __init__(self, upload_bucket: _Optional[str] = ..., endpoint_url: _Optional[str] = ..., region: _Optional[str] = ..., upload_prefix: _Optional[str] = ..., integration: _Optional[_Union[Integration, _Mapping]] = ..., buckets: _Optional[_Iterable[_Union[BucketConfig, _Mapping]]] = ...) -> None: ...

class BenchlingIntegration(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ComputeConfiguration(_message.Message):
    __slots__ = ("log_bucket", "log_prefix", "result_bucket", "result_prefix", "region", "integration")
    LOG_BUCKET_FIELD_NUMBER: _ClassVar[int]
    LOG_PREFIX_FIELD_NUMBER: _ClassVar[int]
    RESULT_BUCKET_FIELD_NUMBER: _ClassVar[int]
    RESULT_PREFIX_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    log_bucket: str
    log_prefix: str
    result_bucket: str
    result_prefix: str
    region: str
    integration: Integration
    def __init__(self, log_bucket: _Optional[str] = ..., log_prefix: _Optional[str] = ..., result_bucket: _Optional[str] = ..., result_prefix: _Optional[str] = ..., region: _Optional[str] = ..., integration: _Optional[_Union[Integration, _Mapping]] = ...) -> None: ...

class ListKeysResponse(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Optional[_Iterable[str]] = ...) -> None: ...

class FeatureFlagsResponse(_message.Message):
    __slots__ = ("flags",)
    class FlagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    flags: _containers.ScalarMap[str, bool]
    def __init__(self, flags: _Optional[_Mapping[str, bool]] = ...) -> None: ...

class ListBucketsResponse(_message.Message):
    __slots__ = ("buckets",)
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    buckets: _containers.RepeatedCompositeFieldContainer[BucketConfig]
    def __init__(self, buckets: _Optional[_Iterable[_Union[BucketConfig, _Mapping]]] = ...) -> None: ...
