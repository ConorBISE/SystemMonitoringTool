from django.http import HttpRequest
from common import api_definitions
from . import models

from ninja import NinjaAPI, Router
from ninja_crud import viewsets, views

api = NinjaAPI()


aggregator_router = Router()


class AggregatorViewSet(viewsets.APIViewSet):
    router = aggregator_router
    model = models.Aggregator
    default_request_body = api_definitions.Aggregator
    default_response_body = api_definitions.Aggregator

    list_aggregators = views.ListView()
    create_aggregators = views.CreateView()

    read_aggregators = views.ReadView(path="/{uuid}")
    update_aggregators = views.UpdateView(path="/{uuid}")
    delete_aggregators = views.DeleteView(path="/{uuid}")


api.add_router("/aggregator/", aggregator_router)

device_router = Router()


class DeviceViewSet(viewsets.APIViewSet):
    router = device_router
    model = models.Device
    default_request_body = api_definitions.Device
    default_response_body = api_definitions.Device

    list_devices = views.ListView()
    create_device = views.CreateView()

    read_devices = views.ReadView(path="/{uuid}")
    update_device = views.UpdateView(path="/{uuid}")
    delete_device = views.DeleteView(path="/{uuid}")


api.add_router("/device/", device_router)


metric_router = Router()


class MetricViewSet(viewsets.APIViewSet):
    router = metric_router
    model = models.Metric
    default_request_body = api_definitions.Metric
    default_response_body = api_definitions.Metric

    list_metrics = views.ListView()
    create_metrics = views.CreateView()

    read_metrics = views.ReadView(path="/{uuid}")
    update_metrics = views.UpdateView(path="/{uuid}")
    delete_metrics = views.DeleteView(path="/{uuid}")


api.add_router("/metric/", metric_router)

metric_reading_router = Router()


class MetricReadingViewSet(viewsets.APIViewSet):
    router = metric_reading_router
    model = models.Reading

    default_request_body = api_definitions.MetricReading
    default_response_body = api_definitions.MetricReading

    list_readings = views.ListView(pagination_class=None)


api.add_router("/metric_reading/", metric_reading_router)


@api.post("/snapshot")
def snapshot(request: HttpRequest, snapshot: api_definitions.Snapshot):
    device = models.Device.objects.get(uuid=snapshot.device.uuid)

    metrics = models.Metric.objects.filter(
        uuid__in=[i.metric.uuid for i in snapshot.readings]
    )

    models.Reading.objects.bulk_create(
        [
            models.Reading(
                metric=metrics.get(uuid=reading.metric.uuid),
                device=device,
                value=reading.value,
                timestamp=reading.timestamp,
            )
            for reading in snapshot.readings
        ]
    )

    return None
