import asyncio
import logging
from typing import List

from aiohttp.web import HTTPException

import common.api_definitions as ad
from collector import config, server_api
from collector.data_source.device_metric_gatherer import DeviceMetricGatherer

logger = logging.getLogger(__name__)


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
                consecutive_failures = 0

                while True:
                    num_metric_readings = queue.qsize()

                    if num_metric_readings > 0:
                        readings = [
                            await queue.get() for _ in range(num_metric_readings)
                        ]

                        snapshot = ad.Snapshot(metric_readings=readings)

                        try:
                            ret = await client.create_snapshot(snapshot)
                            consecutive_failures = 0

                            if ret is None:
                                raise HTTPException()

                        except Exception as e:
                            [queue.put(i) for i in readings]
                            consecutive_failures += 1

                            logger.error(
                                "Failed to post snapshot %s - %d consecutive failures",
                                snapshot,
                                consecutive_failures,
                            )
                            logger.exception(e)

                            if consecutive_failures >= cfg.num_failures_for_backoff:
                                backoff_time = interval * cfg.backoff_intervals
                                logger.error(
                                    "Reached %d consecutive failures - backing off for %d intervals (%d seconds).",
                                    cfg.num_failures_for_backoff,
                                    cfg.backoff_intervals,
                                    backoff_time,
                                )

                                await asyncio.sleep(backoff_time)
                                consecutive_failures = 0

                    await asyncio.sleep(interval)
