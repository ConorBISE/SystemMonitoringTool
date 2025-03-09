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

            if app_data is None or app_data.aggregator.name != cfg.aggregator_name:
                # This is our first run. We'll need to create an aggregator for the first time.
                aggregator = await client.create_aggregator(ad.AggregatorCreationRequest(
                    name=cfg.aggregator_name
                ))

                if aggregator is None:
                    raise ValueError("Error registering aggregator!")

                app_data = config.AppData(aggregator=aggregator)
                config.write_app_data(app_data)
                return aggregator
            else:                
                return app_data.aggregator

    async def run(self):
        aggregator = await self.fetch_or_register_aggregator()
        
        queue: asyncio.Queue[ad.MetricReading] = asyncio.Queue()

        async with asyncio.TaskGroup() as tg:
            ss = SystemStatisticsGatherer(aggregator, queue)
            await ss.init_metrics()
            
            iss = ISSStatisticsGatherer(aggregator, queue)
            await iss.init_metrics()
            
            tg.create_task(ss.run())
            tg.create_task(iss.run())

            async with server_api.APIClient() as client:
                while True:
                    num_metric_readings = queue.qsize()

                    if num_metric_readings > 0:
                        readings = [await queue.get() for _ in range(num_metric_readings)]

                        snapshot = ad.Snapshot(
                            metric_readings=readings
                        )
                        
                        ret = await client.create_snapshot(snapshot)
                        if ret is None:
                            logger.error(f"Failed to post snapshot {snapshot}")

                    await asyncio.sleep(10)


if __name__ == "__main__":
    app = App()
    asyncio.run(app.run())
