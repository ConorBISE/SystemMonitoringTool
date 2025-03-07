from uuid import UUID
from typing import List, TYPE_CHECKING
import datetime
import os

if "DJANGO_SETTINGS_MODULE" in os.environ and not TYPE_CHECKING:
    from ninja import Schema as BaseModel
else:
    from pydantic import BaseModel


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
