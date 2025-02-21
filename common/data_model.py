from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from uuid import UUID, uuid4
from typing import List

@dataclass
class Metric(DataClassJsonMixin):
    name: str
    unit: str

@dataclass
class MetricReading(DataClassJsonMixin):
    metric: Metric
    value: float
    timestamp: int

@dataclass
class Device(DataClassJsonMixin):
    name: str
    uuid: UUID
    
@dataclass
class Snapshot(DataClassJsonMixin):
    device: Device
    readings: List[MetricReading]
    
if __name__ == "__main__":
    snapshot = Snapshot(
        Device("a", uuid4()),
        [
            MetricReading(
                Metric("Temperature", "c"),
                1,
                1000000
            )
        ]
    )
    
    json_text = snapshot.to_json()
    print (json_text)
    print (Snapshot.from_json(json_text))