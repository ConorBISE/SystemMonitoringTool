from rest_framework import serializers

from coreapp.models import Device, Metric, MetricReading

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['name', 'uuid']
        
class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['name', 'unit']
        
class MetricReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricReading
        fields = ['metric', 'device', 'value']