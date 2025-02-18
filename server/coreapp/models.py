from django.db import models

class Device(models.Model):
    name = models.TextField()
    
class Metric(models.Model):
    name = models.TextField()
    unit = models.CharField(max_length=20)
    
class MetricReading(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.FloatField()