from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataType(_message.Message):
    __slots__ = ("id", "unique_id", "label", "description", "filterable_fields", "pipelines", "properties", "config")
    ID_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FILTERABLE_FIELDS_FIELD_NUMBER: _ClassVar[int]
    PIPELINES_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: str
    unique_id: str
    label: str
    description: str
    filterable_fields: _containers.RepeatedScalarFieldContainer[str]
    pipelines: _containers.RepeatedCompositeFieldContainer[DataTypePipeline]
    properties: _containers.RepeatedCompositeFieldContainer[DataTypeProperty]
    config: DataTypeConfig
    def __init__(self, id: _Optional[str] = ..., unique_id: _Optional[str] = ..., label: _Optional[str] = ..., description: _Optional[str] = ..., filterable_fields: _Optional[_Iterable[str]] = ..., pipelines: _Optional[_Iterable[_Union[DataTypePipeline, _Mapping]]] = ..., properties: _Optional[_Iterable[_Union[DataTypeProperty, _Mapping]]] = ..., config: _Optional[_Union[DataTypeConfig, _Mapping]] = ...) -> None: ...

class CreateDataTypeRequest(_message.Message):
    __slots__ = ("unique_id", "label", "description", "config")
    UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    unique_id: str
    label: str
    description: str
    config: DataTypeConfig
    def __init__(self, unique_id: _Optional[str] = ..., label: _Optional[str] = ..., description: _Optional[str] = ..., config: _Optional[_Union[DataTypeConfig, _Mapping]] = ...) -> None: ...

class DataTypePipeline(_message.Message):
    __slots__ = ("pipeline_id", "pipeline_version", "field")
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    pipeline_id: str
    pipeline_version: str
    field: str
    def __init__(self, pipeline_id: _Optional[str] = ..., pipeline_version: _Optional[str] = ..., field: _Optional[str] = ...) -> None: ...

class S3File(_message.Message):
    __slots__ = ("bucket", "key", "upload_url", "download_url")
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    key: str
    upload_url: str
    download_url: str
    def __init__(self, bucket: _Optional[str] = ..., key: _Optional[str] = ..., upload_url: _Optional[str] = ..., download_url: _Optional[str] = ...) -> None: ...

class FileUpload(_message.Message):
    __slots__ = ("filename",)
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    def __init__(self, filename: _Optional[str] = ...) -> None: ...

class InitiateMultipartUpload(_message.Message):
    __slots__ = ("file", "size")
    FILE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    file: S3File
    size: int
    def __init__(self, file: _Optional[_Union[S3File, _Mapping]] = ..., size: _Optional[int] = ...) -> None: ...

class MultipartUploadPart(_message.Message):
    __slots__ = ("file", "upload_id", "part_number")
    FILE_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    file: S3File
    upload_id: str
    part_number: int
    def __init__(self, file: _Optional[_Union[S3File, _Mapping]] = ..., upload_id: _Optional[str] = ..., part_number: _Optional[int] = ...) -> None: ...

class MultiPartUploadInitiated(_message.Message):
    __slots__ = ("upload_id", "first_upload", "parts")
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_UPLOAD_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    first_upload: UploadPartResponse
    parts: _containers.RepeatedCompositeFieldContainer[Part]
    def __init__(self, upload_id: _Optional[str] = ..., first_upload: _Optional[_Union[UploadPartResponse, _Mapping]] = ..., parts: _Optional[_Iterable[_Union[Part, _Mapping]]] = ...) -> None: ...

class Part(_message.Message):
    __slots__ = ("part_number", "size", "etag")
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    part_number: int
    size: int
    etag: str
    def __init__(self, part_number: _Optional[int] = ..., size: _Optional[int] = ..., etag: _Optional[str] = ...) -> None: ...

class UploadPartResponse(_message.Message):
    __slots__ = ("upload_id", "file", "part_number", "upload_url")
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    file: S3File
    part_number: int
    upload_url: str
    def __init__(self, upload_id: _Optional[str] = ..., file: _Optional[_Union[S3File, _Mapping]] = ..., part_number: _Optional[int] = ..., upload_url: _Optional[str] = ...) -> None: ...

class CompleteMultipartUpload(_message.Message):
    __slots__ = ("file", "upload_id", "parts")
    FILE_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    file: S3File
    upload_id: str
    parts: _containers.RepeatedCompositeFieldContainer[Part]
    def __init__(self, file: _Optional[_Union[S3File, _Mapping]] = ..., upload_id: _Optional[str] = ..., parts: _Optional[_Iterable[_Union[Part, _Mapping]]] = ...) -> None: ...

class CompleteMultipartUploadResponse(_message.Message):
    __slots__ = ("file", "success")
    FILE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    file: S3File
    success: bool
    def __init__(self, file: _Optional[_Union[S3File, _Mapping]] = ..., success: bool = ...) -> None: ...

class AbortMultipartUpload(_message.Message):
    __slots__ = ("file", "upload_id")
    FILE_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    file: S3File
    upload_id: str
    def __init__(self, file: _Optional[_Union[S3File, _Mapping]] = ..., upload_id: _Optional[str] = ...) -> None: ...

class AbortMultipartUploadResponse(_message.Message):
    __slots__ = ("file", "success")
    FILE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    file: S3File
    success: bool
    def __init__(self, file: _Optional[_Union[S3File, _Mapping]] = ..., success: bool = ...) -> None: ...

class FastQ(_message.Message):
    __slots__ = ("read_1", "read_2")
    READ_1_FIELD_NUMBER: _ClassVar[int]
    READ_2_FIELD_NUMBER: _ClassVar[int]
    read_1: S3File
    read_2: S3File
    def __init__(self, read_1: _Optional[_Union[S3File, _Mapping]] = ..., read_2: _Optional[_Union[S3File, _Mapping]] = ...) -> None: ...

class BCL(_message.Message):
    __slots__ = ("bcl",)
    BCL_FIELD_NUMBER: _ClassVar[int]
    bcl: S3File
    def __init__(self, bcl: _Optional[_Union[S3File, _Mapping]] = ...) -> None: ...

class Row(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class CSV(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[Row]
    def __init__(self, rows: _Optional[_Iterable[_Union[Row, _Mapping]]] = ...) -> None: ...

class DataTypeConfig(_message.Message):
    __slots__ = ("properties",)
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    properties: _containers.RepeatedCompositeFieldContainer[DataTypeProperty]
    def __init__(self, properties: _Optional[_Iterable[_Union[DataTypeProperty, _Mapping]]] = ...) -> None: ...

class FileConfig(_message.Message):
    __slots__ = ("extensions",)
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    extensions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, extensions: _Optional[_Iterable[str]] = ...) -> None: ...

class DataTypeProperty(_message.Message):
    __slots__ = ("name", "type", "filterable", "file_config")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FILTERABLE_FIELD_NUMBER: _ClassVar[int]
    FILE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    filterable: bool
    file_config: FileConfig
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., filterable: bool = ..., file_config: _Optional[_Union[FileConfig, _Mapping]] = ...) -> None: ...
