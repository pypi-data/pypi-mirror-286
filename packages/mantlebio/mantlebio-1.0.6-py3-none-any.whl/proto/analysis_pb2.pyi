from google.protobuf import timestamp_pb2 as _timestamp_pb2
from proto import common_pb2 as _common_pb2
from proto import entity_pb2 as _entity_pb2
from proto import data_type_pb2 as _data_type_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Analysis(_message.Message):
    __slots__ = ("id", "unique_id", "name", "created_by", "updated_by", "created_at", "updated_at", "inputs", "outputs", "notebook", "status")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Analysis.Status]
        PENDING: _ClassVar[Analysis.Status]
        RUNNING: _ClassVar[Analysis.Status]
        SHUTTING_DOWN: _ClassVar[Analysis.Status]
        COMPLETED: _ClassVar[Analysis.Status]
        ERRORED: _ClassVar[Analysis.Status]
    UNKNOWN: Analysis.Status
    PENDING: Analysis.Status
    RUNNING: Analysis.Status
    SHUTTING_DOWN: Analysis.Status
    COMPLETED: Analysis.Status
    ERRORED: Analysis.Status
    ID_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    unique_id: str
    name: str
    created_by: _common_pb2.User
    updated_by: _common_pb2.User
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    inputs: AnalysisInput
    outputs: AnalysisOutput
    notebook: Notebook
    status: Analysis.Status
    def __init__(self, id: _Optional[str] = ..., unique_id: _Optional[str] = ..., name: _Optional[str] = ..., created_by: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., updated_by: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., inputs: _Optional[_Union[AnalysisInput, _Mapping]] = ..., outputs: _Optional[_Union[AnalysisOutput, _Mapping]] = ..., notebook: _Optional[_Union[Notebook, _Mapping]] = ..., status: _Optional[_Union[Analysis.Status, str]] = ...) -> None: ...

class Notebook(_message.Message):
    __slots__ = ("id", "s3_file", "url", "access_token", "ecs_task_arn", "environment")
    ID_FIELD_NUMBER: _ClassVar[int]
    S3_FILE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ECS_TASK_ARN_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    s3_file: str
    url: str
    access_token: str
    ecs_task_arn: str
    environment: NotebookEnvironment
    def __init__(self, id: _Optional[str] = ..., s3_file: _Optional[str] = ..., url: _Optional[str] = ..., access_token: _Optional[str] = ..., ecs_task_arn: _Optional[str] = ..., environment: _Optional[_Union[NotebookEnvironment, _Mapping]] = ...) -> None: ...

class AnalysisResponse(_message.Message):
    __slots__ = ("analysis",)
    ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    analysis: Analysis
    def __init__(self, analysis: _Optional[_Union[Analysis, _Mapping]] = ...) -> None: ...

class AnalysisList(_message.Message):
    __slots__ = ("analyses",)
    ANALYSES_FIELD_NUMBER: _ClassVar[int]
    analyses: _containers.RepeatedCompositeFieldContainer[Analysis]
    def __init__(self, analyses: _Optional[_Iterable[_Union[Analysis, _Mapping]]] = ...) -> None: ...

class AnalysisValue(_message.Message):
    __slots__ = ("string", "int", "double", "boolean", "s3_file", "entity", "entities", "file_upload")
    STRING_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    BOOLEAN_FIELD_NUMBER: _ClassVar[int]
    S3_FILE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    FILE_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    string: str
    int: int
    double: float
    boolean: bool
    s3_file: _data_type_pb2.S3File
    entity: _entity_pb2.Entity
    entities: _entity_pb2.EntityList
    file_upload: _data_type_pb2.FileUpload
    def __init__(self, string: _Optional[str] = ..., int: _Optional[int] = ..., double: _Optional[float] = ..., boolean: bool = ..., s3_file: _Optional[_Union[_data_type_pb2.S3File, _Mapping]] = ..., entity: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., entities: _Optional[_Union[_entity_pb2.EntityList, _Mapping]] = ..., file_upload: _Optional[_Union[_data_type_pb2.FileUpload, _Mapping]] = ...) -> None: ...

class AnalysisInput(_message.Message):
    __slots__ = ("data",)
    class DataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AnalysisValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[AnalysisValue, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.MessageMap[str, AnalysisValue]
    def __init__(self, data: _Optional[_Mapping[str, AnalysisValue]] = ...) -> None: ...

class AnalysisOutput(_message.Message):
    __slots__ = ("data",)
    class DataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AnalysisValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[AnalysisValue, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.MessageMap[str, AnalysisValue]
    def __init__(self, data: _Optional[_Mapping[str, AnalysisValue]] = ...) -> None: ...

class CreateAnalysisRequest(_message.Message):
    __slots__ = ("name", "status", "inputs", "environment")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: Analysis.Status
    inputs: AnalysisInput
    environment: NotebookEnvironment
    def __init__(self, name: _Optional[str] = ..., status: _Optional[_Union[Analysis.Status, str]] = ..., inputs: _Optional[_Union[AnalysisInput, _Mapping]] = ..., environment: _Optional[_Union[NotebookEnvironment, _Mapping]] = ...) -> None: ...

class AnalysisStatusUpdateRequest(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: Analysis.Status
    def __init__(self, status: _Optional[_Union[Analysis.Status, str]] = ...) -> None: ...

class AddNotebookRequest(_message.Message):
    __slots__ = ("url", "s3_file", "access_token", "ecs_task_arn", "environment")
    URL_FIELD_NUMBER: _ClassVar[int]
    S3_FILE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ECS_TASK_ARN_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    url: str
    s3_file: str
    access_token: str
    ecs_task_arn: str
    environment: NotebookEnvironment
    def __init__(self, url: _Optional[str] = ..., s3_file: _Optional[str] = ..., access_token: _Optional[str] = ..., ecs_task_arn: _Optional[str] = ..., environment: _Optional[_Union[NotebookEnvironment, _Mapping]] = ...) -> None: ...

class UpdateNotebookTaskRequest(_message.Message):
    __slots__ = ("url", "access_token", "ecs_task_arn", "environment")
    URL_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ECS_TASK_ARN_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    url: str
    access_token: str
    ecs_task_arn: str
    environment: NotebookEnvironment
    def __init__(self, url: _Optional[str] = ..., access_token: _Optional[str] = ..., ecs_task_arn: _Optional[str] = ..., environment: _Optional[_Union[NotebookEnvironment, _Mapping]] = ...) -> None: ...

class CreateNotebookEnvironmentRequest(_message.Message):
    __slots__ = ("environment_name", "pip_requirements", "conda_requirements", "github_requirements", "cpu", "memory", "ecr_path", "version")
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    PIP_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    CONDA_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    GITHUB_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    ECR_PATH_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    environment_name: str
    pip_requirements: _containers.RepeatedScalarFieldContainer[str]
    conda_requirements: _containers.RepeatedScalarFieldContainer[str]
    github_requirements: _containers.RepeatedScalarFieldContainer[str]
    cpu: int
    memory: int
    ecr_path: str
    version: str
    def __init__(self, environment_name: _Optional[str] = ..., pip_requirements: _Optional[_Iterable[str]] = ..., conda_requirements: _Optional[_Iterable[str]] = ..., github_requirements: _Optional[_Iterable[str]] = ..., cpu: _Optional[int] = ..., memory: _Optional[int] = ..., ecr_path: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class NotebookEnvironment(_message.Message):
    __slots__ = ("environment_name", "tenant_id", "created_by", "updated_by", "pip_requirements", "conda_requirements", "github_requirements", "tag_name", "ecs_task_arn", "status", "cpu", "memory", "created_at", "updated_at", "id", "ecr_url", "version")
    class EnvironmentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[NotebookEnvironment.EnvironmentStatus]
        ACTIVE: _ClassVar[NotebookEnvironment.EnvironmentStatus]
        PENDING: _ClassVar[NotebookEnvironment.EnvironmentStatus]
        ERRORED: _ClassVar[NotebookEnvironment.EnvironmentStatus]
    INVALID: NotebookEnvironment.EnvironmentStatus
    ACTIVE: NotebookEnvironment.EnvironmentStatus
    PENDING: NotebookEnvironment.EnvironmentStatus
    ERRORED: NotebookEnvironment.EnvironmentStatus
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    PIP_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    CONDA_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    GITHUB_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    TAG_NAME_FIELD_NUMBER: _ClassVar[int]
    ECS_TASK_ARN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ECR_URL_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    environment_name: str
    tenant_id: str
    created_by: _common_pb2.User
    updated_by: _common_pb2.User
    pip_requirements: _containers.RepeatedScalarFieldContainer[str]
    conda_requirements: _containers.RepeatedScalarFieldContainer[str]
    github_requirements: _containers.RepeatedScalarFieldContainer[str]
    tag_name: str
    ecs_task_arn: str
    status: NotebookEnvironment.EnvironmentStatus
    cpu: int
    memory: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    id: str
    ecr_url: str
    version: str
    def __init__(self, environment_name: _Optional[str] = ..., tenant_id: _Optional[str] = ..., created_by: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., updated_by: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., pip_requirements: _Optional[_Iterable[str]] = ..., conda_requirements: _Optional[_Iterable[str]] = ..., github_requirements: _Optional[_Iterable[str]] = ..., tag_name: _Optional[str] = ..., ecs_task_arn: _Optional[str] = ..., status: _Optional[_Union[NotebookEnvironment.EnvironmentStatus, str]] = ..., cpu: _Optional[int] = ..., memory: _Optional[int] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., ecr_url: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class ListNotebookEnvironmentResponse(_message.Message):
    __slots__ = ("environments",)
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    environments: _containers.RepeatedCompositeFieldContainer[NotebookEnvironment]
    def __init__(self, environments: _Optional[_Iterable[_Union[NotebookEnvironment, _Mapping]]] = ...) -> None: ...
