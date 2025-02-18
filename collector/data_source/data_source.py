import asyncio
from asyncio import Queue
from typing import Any, List

from common.data_model import MetricReading

class MetricsGatherer:
    def __init__(self, queue: Queue):
        self.queue = queue
        
    async def gather_data(self) -> List[MetricReading]:
        raise NotImplementedError()
        
    async def run(self, interval: float=5):
        while True:
            await self.queue.put(await self.gather_data())
            await asyncio.sleep(interval)