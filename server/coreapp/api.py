from common import api_definitions
from . import models

from ninja import NinjaAPI
from typing import List

api = NinjaAPI()


@api.get("/devices", response=List[api_definitions.Device])
def devices(request):
    return models.Device.objects.all()
