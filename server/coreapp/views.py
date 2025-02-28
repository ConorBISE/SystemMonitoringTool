from rest_framework import viewsets

from coreapp.models import Device, Metric, MetricReading
from coreapp.serializers import (DeviceSerializer,
                                        MetricReadingSerializer,
                                        MetricSerializer)


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    
class MetricReadingViewSet(viewsets.ModelViewSet):
    queryset = MetricReading.objects.all()
    serializer_class = MetricReadingSerializer