from django.http import HttpRequest
from common import api_definitions
from . import models

from ninja import NinjaAPI, Router
from ninja_crud import viewsets, views

api = NinjaAPI()


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


api.add_router("/device", device_router)


metric_router = Router()


class MetricViewSet(viewsets.APIViewSet):
    router = metric_router
    model = models.Metric
    default_request_body = api_definitions.Metric
    default_response_body = api_definitions.Metric

    list_devices = views.ListView()
    create_device = views.CreateView()

    read_devices = views.ReadView(path="/{uuid}")
    update_device = views.UpdateView(path="/{uuid}")
    delete_device = views.DeleteView(path="/{uuid}")


api.add_router("/metric", metric_router)


@api.post("/snapshot")
def snapshot(request: HttpRequest, snapshot: api_definitions.Snapshot):
    device = models.Device.objects.get(uuid=snapshot.device.uuid)

    metrics = models.Metric.objects.filter(uuid__in=[i.metric.uuid for i in snapshot.readings])

    models.MetricReading.objects.bulk_create(
        [
            models.MetricReading(
                metric=metrics.get(uuid=reading.metric.uuid),
                device=device,
                value=reading.value,
            )
            for reading in snapshot.readings
        ]
    )

    return None
