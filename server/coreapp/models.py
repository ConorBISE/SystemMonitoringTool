from django.db import models


class Device(models.Model):
    name = models.TextField()
    uuid = models.UUIDField(unique=True)


class Metric(models.Model):
    name = models.TextField()
    unit = models.CharField(max_length=20)
    uuid = models.UUIDField(unique=True)


class MetricReading(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField()