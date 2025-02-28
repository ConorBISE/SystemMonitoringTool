from django.urls import include, path
from rest_framework import routers

from coreapp import views

router = routers.DefaultRouter()
router.register('devices', views.DeviceViewSet)
router.register('metrics', views.MetricViewSet)
router.register('metric_readings', views.MetricReadingViewSet)

urlpatterns = [
    path('', include(router.urls))
]
