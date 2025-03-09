from uuid import UUID, uuid4

import aiohttp
import collector.server_api as server_api 
import common.api_definitions as ad 
from .data_source.system_statistics import SystemStatisticsGatherer
from .data_source.iss import ISSStatisticsGatherer
from . import config

import logging
import asyncio

logger = logging.getLogger(__name__)
config.setup_logging()

cfg = config.load_config()

class App:
    def __init__(self):
        pass

    async def fetch_or_register_aggregator(self):
        async with server_api.APIClient() as client:
            app_data = config.read_app_data()

            if app_data is None:
                # This is our first run. We'll need to create an aggregator for the first time.
                aggregator = ad.Aggregator(
                    name=cfg.aggregator_name,
                    uuid=uuid4() # TODO - this should be generated server-side
                )
                
                await client.create_aggregator(aggregator)

                app_data = config.AppData(aggregator=aggregator)
                config.write_app_data(app_data)
                return aggregator
            else:
                if app_data.aggregator.name != cfg.aggregator_name:
                    app_data.aggregator.name = cfg.aggregator_name
                    await client.update_aggregator(app_data.aggregator.uuid, app_data.aggregator)
                    config.write_app_data(app_data)
                
                return app_data.aggregator

    async def run(self):
        await self.fetch_or_register_aggregator()
        
        queue: asyncio.Queue[ad.MetricReading] = asyncio.Queue()
        guid = UUID('e234c36a-a70b-4015-bfad-2ac334352a59')

        async with asyncio.TaskGroup() as tg:
            tg.create_task(SystemStatisticsGatherer(queue).run())
            tg.create_task(ISSStatisticsGatherer(queue).run())

            async with server_api.APIClient() as client:
                while True:
                    num_metric_readings = queue.qsize()

                    if num_metric_readings > 0:
                        readings = [await queue.get() for _ in range(num_metric_readings)]

                        snapshot = ad.Snapshot(
                            device=ad.Device(name="Paige", uuid=guid), readings=readings
                        )
                        
                        ret = await client.create_snapshot(snapshot)
                        if ret is None:
                            logger.error(f"Failed to post snapshot {snapshot}")

                    await asyncio.sleep(10)


if __name__ == "__main__":
    app = App()
    asyncio.run(app.run())
