import logging
import time
from typing import List
from uuid import UUID

import psutil

from collector.data_source.data_source import MetricsGatherer
from common.api_definitions import Metric, MetricReading

logger = logging.getLogger(__name__)


def battery_percentage() -> int | None:
    battery = psutil.sensors_battery()

    if battery is None:
        return None

    return battery.percent


def cpu_usage() -> float:
    return psutil.cpu_percent()


class SystemStatisticsGatherer(MetricsGatherer):
    # TODO: how do we sync these with the server-side definition of a metric?
    BATTERY_PERCENTAGE_METRIC = Metric(
        name="Battery Percentage",
        unit="%",
        uuid=UUID("627524da-4a33-4dd5-a7ab-26ab88f1f549", version=4),
    )

    CPU_USAGE_METRIC = Metric(
        name="CPU Usage",
        unit="%",
        uuid=UUID("548d8eea-d100-4fe9-8357-30ae804eedd7", version=4),
    )

    async def gather_data(self) -> List[MetricReading]:
        timestamp = int(time.time())

        battery = battery_percentage()
        cpu = cpu_usage()

        metrics = [
            MetricReading(metric=self.CPU_USAGE_METRIC, value=cpu, timestamp=timestamp)
        ]

        if battery is not None:
            metrics.append(
                MetricReading(
                    metric=self.BATTERY_PERCENTAGE_METRIC,
                    value=battery,
                    timestamp=timestamp,
                )
            )
        else:
            logger.error("Error getting battery percentage! None returned.")

        return metrics
