import asyncio
from asyncio import Queue
import logging
from typing import Any, List

from collector.server_api import APIClient
from common.api_definitions import Aggregator, Device, DeviceCreationRequest, Metric, MetricCreationRequest, MetricReading

logger = logging.getLogger(__name__)


class DeviceMetricGatherer:
    NAME = "DeviceMetricGatherer"
    
    def __init__(self, aggregator: Aggregator, queue: Queue):
        self.aggregator = aggregator
        self.queue = queue
        self._device = None

    @property
    def device_creation_request(self) -> DeviceCreationRequest:
        return DeviceCreationRequest(
            name=self.NAME,
            aggregator_id=self.aggregator.uuid
        )
        
    async def find_create_device(self, device_creation_request: DeviceCreationRequest) -> Device:
        async with APIClient() as client:
            device_list = await client.get_device_by_name_and_aggregator(device_creation_request.name, device_creation_request.aggregator_id)

            if device_list is None:
                raise ValueError("Error determining existance of device %s", device_creation_request)
            
            if device_list.count > 0:
                device = device_list.items[0]
            else:
                # We're going to need to create a device
                device = await client.create_device(device_creation_request)
                
                if device is None:
                    raise ValueError("Error creating device %s", device_creation_request)
                
            return device

    @property
    async def device(self) -> Device:
        if self._device is None:
            self._device = await self.find_create_device(self.device_creation_request)

        return self._device

        
    async def find_create_metric(self, metric_creation_request: MetricCreationRequest) -> Metric:
        async with APIClient() as client:
            metric_list = await client.get_metric_by_name_and_unit(metric_creation_request.name, metric_creation_request.unit)

            if metric_list is None:
                raise ValueError("Error determining existance of metric %s", metric_creation_request)
            
            if metric_list.count > 0:
                metric = metric_list.items[0]
            else:
                # We're going to need to create a device
                metric = await client.create_metric(metric_creation_request)
                
                if metric is None:
                    raise ValueError("Error creating metric %s", metric_creation_request)
                
            return metric

    async def gather_data(self) -> List[MetricReading]:
        raise NotImplementedError()

    async def run(self, interval: float = 5):
        while True:
            [await self.queue.put(i) for i in await self.gather_data()]
            await asyncio.sleep(interval)
