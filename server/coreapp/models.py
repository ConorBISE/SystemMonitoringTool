import uuid

from django.db import models


class Aggregator(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.TextField()


class Device(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.TextField()
    aggregator = models.ForeignKey(Aggregator, on_delete=models.CASCADE)


class Metric(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.TextField()
    unit = models.CharField(max_length=20)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)


class Reading(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField()
