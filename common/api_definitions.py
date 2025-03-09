from uuid import UUID
from typing import Generic, List, TYPE_CHECKING, TypeVar
import datetime
import os

if "DJANGO_SETTINGS_MODULE" in os.environ and not TYPE_CHECKING:
    from ninja import Schema as BaseModel
else:
    from pydantic import BaseModel


class Aggregator(BaseModel):
    name: str
    uuid: UUID


class Metric(BaseModel):
    name: str
    unit: str
    uuid: UUID


class MetricReading(BaseModel):
    metric: Metric
    value: float
    timestamp: datetime.datetime


class Device(BaseModel):
    name: str
    uuid: UUID


class Snapshot(BaseModel):
    device: Device
    readings: List[MetricReading]

T = TypeVar("T")

class ListResponse(BaseModel, Generic[T]):
    items: List[T]
    count: int