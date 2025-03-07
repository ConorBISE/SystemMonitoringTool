import asyncio
from asyncio import Queue
from typing import Any, List

from common.api_definitions import MetricReading


class MetricsGatherer:
    def __init__(self, queue: Queue):
        self.queue = queue

    async def gather_data(self) -> List[MetricReading]:
        raise NotImplementedError()

    async def run(self, interval: float = 5):
        while True:
            [await self.queue.put(i) for i in await self.gather_data()]
            await asyncio.sleep(interval)
