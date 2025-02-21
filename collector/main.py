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

async def main():
    queue: asyncio.Queue[MetricReading] = asyncio.Queue()
    
    guid = uuid4()
    
    async with asyncio.TaskGroup() as tg:
        tg.create_task(SystemStatisticsGatherer(queue).run())
        tg.create_task(ISSStatisticsGatherer(queue).run())

        async with aiohttp.ClientSession() as client_session:
            while True:
                num_metric_readings = queue.qsize()

                if num_metric_readings > 0:
                    readings = [await queue.get() for _ in range(num_metric_readings)]

                    snapshot = Snapshot(
                        Device("Paige", guid),
                        readings
                    )
                    
                    await client_session.post("https://webhook.site/9799e737-9c0c-4a0b-b9fd-21d5b769e965", data=snapshot.to_json(), headers={"Content-Type": "application/json"})

                await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())