from dataclasses import dataclass
from dataclasses_json import dataclass_json

from uuid import UUID, uuid4
from typing import List

@dataclass_json
@dataclass
class Metric:
    name: str
    unit: str

@dataclass_json
@dataclass
class MetricReading:
    metric: Metric
    value: float
    timestamp: int

@dataclass_json
@dataclass
class Device:
    name: str
    uuid: UUID
    
@dataclass_json
@dataclass
class Snapshot:
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