from django.db import models


class Aggregator(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.TextField()


class Device(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.TextField()
    aggregator = models.ForeignKey(Aggregator, on_delete=models.CASCADE)


class Metric(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.TextField()
    unit = models.CharField(max_length=20)


class Reading(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField()
