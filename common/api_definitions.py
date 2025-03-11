import enum
from uuid import UUID
from typing import Any, Generic, List, TYPE_CHECKING, TypeVar
import datetime
import os

if "DJANGO_SETTINGS_MODULE" in os.environ and not TYPE_CHECKING:
    from ninja import Schema as BaseModel
else:
    from pydantic import BaseModel


class OptionalModel(BaseModel):
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)

        for field in cls.model_fields.values():
            field.default = None

        cls.model_rebuild(force=True)


class AggregatorCreationRequest(BaseModel):
    name: str


class Aggregator(AggregatorCreationRequest):
    uuid: UUID


class DeviceCreationRequest(BaseModel):
    name: str
    aggregator_id: UUID


class Device(DeviceCreationRequest):
    uuid: UUID


class DeviceQueryParams(Device, OptionalModel): ...


class MetricCreationRequest(BaseModel):
    name: str
    unit: str
    device_id: UUID


class Metric(MetricCreationRequest):
    uuid: UUID


class MetricQueryParams(Metric, OptionalModel): ...


class MetricReading(BaseModel):
    metric_id: UUID
    value: float
    timestamp: datetime.datetime


class MetricReadingQueryParams(MetricReading, OptionalModel): ...


class Snapshot(BaseModel):
    metric_readings: List[MetricReading]


class ControlCommand(enum.StrEnum):
    OpenBrowser = "open_browser"


class ControlMessage(BaseModel):
    command: ControlCommand
    data: str


T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    items: List[T]
    count: int
