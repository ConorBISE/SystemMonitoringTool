from typing import List
from collector.data_source.device_metric_gatherer import DeviceMetricGatherer
import collector.server_api as server_api
import common.api_definitions as ad
from . import config

import logging
import asyncio
import importlib

logger = logging.getLogger(__name__)
config.setup_logging()

cfg = config.load_config()


class AggregatorPoller:
    def __init__(
        self, aggregator: ad.Aggregator, gatherers: List[type[DeviceMetricGatherer]]
    ):
        self.aggregator = aggregator
        self.gatherer_classes = gatherers

    async def run(self, interval: float = 10):
        queue: asyncio.Queue[ad.MetricReading] = asyncio.Queue()
        aggregators = [i(self.aggregator, queue) for i in self.gatherer_classes]

        async with asyncio.TaskGroup() as tg:
            for aggregator in aggregators:
                await aggregator.init_metrics()
                tg.create_task(aggregator.run())

            async with server_api.APIClient() as client:
                while True:
                    num_metric_readings = queue.qsize()

                    if num_metric_readings > 0:
                        readings = [
                            await queue.get() for _ in range(num_metric_readings)
                        ]

                        snapshot = ad.Snapshot(metric_readings=readings)

                        ret = await client.create_snapshot(snapshot)
                        if ret is None:
                            logger.error(f"Failed to post snapshot {snapshot}")

                    await asyncio.sleep(interval)


def lookup_gatherer(path: str) -> type[DeviceMetricGatherer]:
    try:
        module_path, class_name = path.rsplit(".", 1)
    except ValueError:
        raise ImportError("Invalid module path %s", path)
    
    module = importlib.import_module(module_path)
    
    try:
        cls = getattr(module, class_name)
    except AttributeError:
        raise ImportError("Module %s has no class %s", module_path, class_name)
    
    if not issubclass(cls, DeviceMetricGatherer):
        raise ValueError("%s is not a DeviceMetricGatherer", path)
    
    return cls


class App:
    def __init__(self):
        pass

    async def fetch_or_register_aggregator(self):
        async with server_api.APIClient() as client:
            app_data = config.read_app_data()

            if app_data is None or app_data.aggregator.name != cfg.aggregator_name:
                # This is our first run. We'll need to create an aggregator for the first time.
                aggregator = await client.create_aggregator(
                    ad.AggregatorCreationRequest(name=cfg.aggregator_name)
                )

                if aggregator is None:
                    raise ValueError("Error registering aggregator!")

                app_data = config.AppData(aggregator=aggregator)
                config.write_app_data(app_data)
                return aggregator
            else:
                return app_data.aggregator

    async def run(self):
        aggregator = await self.fetch_or_register_aggregator()

        gatherer_classes = list(map(lookup_gatherer, cfg.device_gatherer_classes))
        agg_poller = AggregatorPoller(aggregator, gatherer_classes)

        await agg_poller.run()


if __name__ == "__main__":
    app = App()
    asyncio.run(app.run())
