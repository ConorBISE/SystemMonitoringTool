from uuid import UUID
from typing import Any, Generic, List, TYPE_CHECKING, Optional, TypeVar
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


class MetricCreationRequest(BaseModel):
    name: str
    unit: str


class Metric(MetricCreationRequest):
    uuid: UUID


class MetricQueryParams(Metric, OptionalModel):
    ...

class DeviceCreationRequest(BaseModel):
    name: str
    aggregator_id: UUID


class Device(DeviceCreationRequest):
    uuid: UUID


class DeviceQueryParams(Metric, OptionalModel):
    ...


class MetricReading(BaseModel):
    metric: Metric
    device: Device
    value: float
    timestamp: datetime.datetime


class Snapshot(BaseModel):
    metric_readings: List[MetricReading]


T = TypeVar("T")


class ListResponse(BaseModel, Generic[T]):
    items: List[T]
    count: int
