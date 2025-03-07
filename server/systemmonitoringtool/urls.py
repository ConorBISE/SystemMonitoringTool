from django.urls import include, path

from server.coreapp.api import api

urlpatterns = [path("api/", api.urls)]
