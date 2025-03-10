from django.urls import path

from server.coreapp.api import api

urlpatterns = [path("api/", api.urls)]
