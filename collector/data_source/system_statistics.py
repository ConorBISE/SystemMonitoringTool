import datetime
import logging
from typing import List

import psutil

from collector.data_source.device_metric_gatherer import DeviceMetricGatherer
import common.api_definitions as ad

logger = logging.getLogger(__name__)


def battery_percentage() -> int | None:
    battery = psutil.sensors_battery()

    if battery is None:
        return None

    return battery.percent


def cpu_usage() -> float:
    return psutil.cpu_percent()


class SystemStatisticsGatherer(DeviceMetricGatherer):
    NAME = "System Statistics"

    async def init_metrics(self):
        self.BATTERY_PERCENTAGE_METRIC = await self.find_create_metric(
            ad.MetricCreationRequest(name="Battery Percentage", unit="%")
        )

        self.CPU_USAGE_METRIC = await self.find_create_metric(
            ad.MetricCreationRequest(
                name="CPU Usage",
                unit="%",
            )
        )

    async def gather_data(self) -> List[ad.MetricReading]:
        timestamp = datetime.datetime.now()

        battery = battery_percentage()
        cpu = cpu_usage()

        metrics = [
            ad.MetricReading(
                metric_id=self.CPU_USAGE_METRIC.uuid,
                value=cpu,
                timestamp=timestamp,
                device_id=(await self.device).uuid,
            )
        ]

        if battery is not None:
            metrics.append(
                ad.MetricReading(
                    metric_id=self.BATTERY_PERCENTAGE_METRIC.uuid,
                    value=battery,
                    timestamp=timestamp,
                    device_id=(await self.device).uuid,
                )
            )
        else:
            logger.error("Error getting battery percentage! None returned.")

        return metrics
