import asyncio
import importlib
import logging
import os
import sys
import webbrowser

import collector.server_api as server_api
import common.api_definitions as ad
from collector.aggregator_poller import AggregatorPoller
from collector.control_channel import ControlChannelListener
from collector.data_source.device_metric_gatherer import DeviceMetricGatherer

from . import config

logger = logging.getLogger(__name__)
config.setup_logging()

cfg = config.load_config()


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


def open_browser(message: ad.ControlMessage):
    logger.info("Received command to open %s", message.data)
    webbrowser.open(message.data)


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

        await asyncio.gather(
            agg_poller.run(interval=1),
            ControlChannelListener(
                aggregator, {ad.ControlCommand.OpenBrowser: open_browser}
            ).run(),
        )


if __name__ == "__main__":
    app = App()
    asyncio.run(app.run())
