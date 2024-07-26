from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[JobStatus]
    PENDING: _ClassVar[JobStatus]
    RUNNING: _ClassVar[JobStatus]
    COMPLETED: _ClassVar[JobStatus]
    FAILED: _ClassVar[JobStatus]
    CANCELED: _ClassVar[JobStatus]

UNKNOWN: JobStatus
PENDING: JobStatus
RUNNING: JobStatus
COMPLETED: JobStatus
FAILED: JobStatus
CANCELED: JobStatus

class JobRequest(_message.Message):
    __slots__ = (
        'job_data',
        'detach',
        'direct_connect_logs',
        'args',
        'status',
        'scheduled_runner_id',
        'physical_plan_v2',
        'scheduling_error',
    )
    JOB_DATA_FIELD_NUMBER: _ClassVar[int]
    DETACH_FIELD_NUMBER: _ClassVar[int]
    DIRECT_CONNECT_LOGS_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_RUNNER_ID_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_PLAN_V2_FIELD_NUMBER: _ClassVar[int]
    SCHEDULING_ERROR_FIELD_NUMBER: _ClassVar[int]
    job_data: str
    detach: bool
    direct_connect_logs: bool
    args: _containers.RepeatedCompositeFieldContainer[JobArg]
    status: JobStatus
    scheduled_runner_id: str
    physical_plan_v2: bytes
    scheduling_error: str
    def __init__(
        self,
        job_data: _Optional[str] = ...,
        detach: bool = ...,
        direct_connect_logs: bool = ...,
        args: _Optional[_Iterable[_Union[JobArg, _Mapping]]] = ...,
        status: _Optional[_Union[JobStatus, str]] = ...,
        scheduled_runner_id: _Optional[str] = ...,
        physical_plan_v2: _Optional[bytes] = ...,
        scheduling_error: _Optional[str] = ...,
    ) -> None: ...

class JobArg(_message.Message):
    __slots__ = ('key', 'value')
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
