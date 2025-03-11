import datetime
from typing import List, Optional
from uuid import UUID

from channels.layers import get_channel_layer
from django.http import HttpRequest
from ninja import Field, FilterSchema, NinjaAPI, Query, Router
from ninja_crud import views, viewsets

from common import api_definitions as ad

from . import models

api = NinjaAPI()


aggregator_router = Router()


class AggregatorViewSet(viewsets.APIViewSet):
    router = aggregator_router
    model = models.Aggregator
    default_request_body = ad.Aggregator
    default_response_body = ad.Aggregator

    list_aggregators = views.ListView()
    create_aggregators = views.CreateView(request_body=ad.AggregatorCreationRequest)

    read_aggregators = views.ReadView(path="/{uuid}")
    update_aggregators = views.UpdateView(path="/{uuid}")
    delete_aggregators = views.DeleteView(path="/{uuid}")


api.add_router("/aggregator/", aggregator_router)

device_router = Router()


class DeviceViewSet(viewsets.APIViewSet):
    router = device_router
    model = models.Device
    default_request_body = ad.Device
    default_response_body = ad.Device

    list_devices = views.ListView(query_parameters=ad.DeviceQueryParams)
    create_device = views.CreateView(request_body=ad.DeviceCreationRequest)

    read_devices = views.ReadView(path="/{uuid}")
    update_device = views.UpdateView(path="/{uuid}")
    delete_device = views.DeleteView(path="/{uuid}")


api.add_router("/device/", device_router)


metric_router = Router()


class MetricViewSet(viewsets.APIViewSet):
    router = metric_router
    model = models.Metric
    default_request_body = ad.Metric
    default_response_body = ad.Metric

    list_metrics = views.ListView(query_parameters=ad.MetricQueryParams)
    create_metrics = views.CreateView(request_body=ad.MetricCreationRequest)

    read_metrics = views.ReadView(path="/{uuid}")
    update_metrics = views.UpdateView(path="/{uuid}")
    delete_metrics = views.DeleteView(path="/{uuid}")


api.add_router("/metric/", metric_router)

metric_reading_router = Router()


class MetricReadingFilter(FilterSchema):
    metric_id: Optional[UUID] = None
    timestamp_min: Optional[datetime.datetime] = Field(None, q="timestamp__gt")  # type: ignore
    timestamp_max: Optional[datetime.datetime] = Field(None, q="timestamp__lt")  # type: ignore


@api.get("/metric_reading/", response=List[ad.MetricReading])
def metric_reading(request: HttpRequest, filters: Query[MetricReadingFilter]):
    readings = models.Reading.objects.all()
    readings = filters.filter(readings).all()
    return readings


@api.post("/snapshot")
def snapshot(request: HttpRequest, snapshot: ad.Snapshot):
    models.Reading.objects.bulk_create(
        [
            models.Reading(
                metric_id=reading.metric_id,
                device_id=reading.device_id,
                value=reading.value,
                timestamp=reading.timestamp,
            )
            for reading in snapshot.metric_readings
        ]
    )

    return snapshot


@api.post("/aggregator/{aggregator_id}/control")
async def control(
    request: HttpRequest, aggregator_id: UUID, control_message: ad.ControlMessage
):
    channel_layer = get_channel_layer()

    group_name = f"control_{aggregator_id}"

    if channel_layer is not None:
        await channel_layer.group_send(
            group_name,
            {"type": "control.message", "message": control_message.model_dump_json()},
        )
