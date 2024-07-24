from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UploadFileRequest(_message.Message):
    __slots__ = ("hash_md5", "file_name", "project_id")
    HASH_MD5_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    hash_md5: str
    file_name: str
    project_id: str
    def __init__(self, hash_md5: _Optional[str] = ..., file_name: _Optional[str] = ..., project_id: _Optional[str] = ...) -> None: ...

class UploadFileResponse(_message.Message):
    __slots__ = ("signed_url",)
    SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    signed_url: str
    def __init__(self, signed_url: _Optional[str] = ...) -> None: ...
