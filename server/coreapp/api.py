from django.http import HttpRequest
from common import api_definitions as ad
from . import models

from ninja import NinjaAPI, Router
from ninja_crud import viewsets, views

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


class MetricReadingViewSet(viewsets.APIViewSet):
    router = metric_reading_router
    model = models.Reading

    default_request_body = ad.MetricReading
    default_response_body = ad.MetricReading

    list_readings = views.ListView(pagination_class=None)


api.add_router("/metric_reading/", metric_reading_router)


@api.post("/snapshot")
def snapshot(request: HttpRequest, snapshot: ad.Snapshot):    
    models.Reading.objects.bulk_create(
        [
            models.Reading(
                metric_id=reading.metric.uuid,
                device_id=reading.device.uuid, 
                value=reading.value,
                timestamp=reading.timestamp
            ) for reading in snapshot.metric_readings
        ]
    )

    return snapshot
