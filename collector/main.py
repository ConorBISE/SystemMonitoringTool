from uuid import uuid4

import aiohttp
from common.data_model import Device, MetricReading, Snapshot
from .data_source.system_statistics import SystemStatisticsGatherer
from .data_source.iss import ISSStatisticsGatherer
from . import config

import logging
import asyncio

logger = logging.getLogger(__name__)
config.setup_logging()

cfg = config.load_config()

async def iss_data_gathering_task(queue: asyncio.Queue[int]):
    while True:
        await queue.put(42)
        await asyncio.sleep(1)

async def main():
    queue: asyncio.Queue[MetricReading] = asyncio.Queue()
    
    async with asyncio.TaskGroup() as tg:
        tg.create_task(SystemStatisticsGatherer(queue).run())
        tg.create_task(ISSStatisticsGatherer(queue).run())

        async with aiohttp.ClientSession() as client_session:
            while True:
                num_metric_readings = queue.qsize()
                readings = [await queue.get() for _ in range(num_metric_readings)]

                snapshot = Snapshot(
                    Device("Paige", uuid4()),
                    readings
                )
                
                await client_session.post("https://webhook.site/f9d83964-9c1a-4e7d-8c32-542ba3d79814", data=snapshot.to_json(), headers={"Content-Type": "application/json"})
                await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())