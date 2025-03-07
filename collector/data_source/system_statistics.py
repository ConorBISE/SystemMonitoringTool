import psutil

from typing import List
import time
import logging

from collector.data_source.data_source import MetricsGatherer
from common.api_definitions import Metric, MetricReading

logger = logging.getLogger(__name__)


def battery_percentage() -> int | None:
    battery = psutil.sensors_battery()

    if battery is None:
        return None

    return battery.percent


def cpu_usage() -> float | None:
    return psutil.cpu_percent()


class SystemStatisticsGatherer(MetricsGatherer):
    # TODO: how do we sync these with the server-side definition of a metric?
    BATTERY_PERCENTAGE_METRIC = Metric(name="Battery Percentage", unit="%")

    CPU_USAGE_METRIC = Metric(name="CPU Usage", unit="%")

    async def gather_data(self) -> List[MetricReading]:
        timestamp = int(time.time())

        battery = battery_percentage()
        cpu = cpu_usage()

        metrics = []

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

        if cpu is not None:
            metrics.append(
                MetricReading(
                    metric=self.CPU_USAGE_METRIC, value=cpu, timestamp=timestamp
                )
            )
        else:
            logger.error("Error getting CPU usage percentage! None returned.")

        return metrics
