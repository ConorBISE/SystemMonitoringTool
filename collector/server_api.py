import functools
import inspect
import logging
from types import UnionType
from typing import Self, get_args
import urllib.parse
from uuid import UUID

import aiohttp

from collector import config
from common import api_definitions as ad

logger = logging.getLogger(__name__)
cfg = config.load_config()


class APIClient:
    async def __aenter__(self) -> Self:
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        if self.session:
            await self.session.close()
        self.session = None

    @staticmethod
    def request(method: str, url: str):
        if url.startswith("/"):
            url = url[1:]

        def decorator(wrapped):
            arg_names = list(inspect.signature(wrapped).parameters)[1:]

            async def inner(self: Self, *args):
                formatted_url = url.format(
                    **{arg_name: value for (arg_name, value) in zip(arg_names, args)}
                )

                full_url = urllib.parse.urljoin(cfg.server_url, formatted_url)

                body = None
                if "body" in arg_names:
                    body = args[arg_names.index("body")].model_dump_json()

                if self.session is None:
                    raise ValueError(
                        "APIClient methods must be used inside an APIClient context manager!"
                    )

                res = await self.session.request(
                    method,
                    full_url,
                    data=body,
                    headers={"Content-Type": "application/json"} if body else {},
                )

                if res.status < 200 or res.status > 299:
                    logger.error(f"Failed to make {method} request {full_url}:")
                    logger.error(res)
                    return None

                return_type = wrapped.__annotations__["return"]

                if isinstance(return_type, UnionType):
                    return_type = get_args(return_type)[0]

                return return_type.model_validate_json(await res.text())

            return inner

        return decorator

    get = functools.partial(request, "get")
    post = functools.partial(request, "post")
    put = functools.partial(request, "put")

    @get("/device?name={name}&aggregator_id={aggregator_id}")
    async def get_device_by_name_and_aggregator(
        self, name: str, aggregator_id: UUID
    ) -> ad.ListResponse[ad.Device] | None: ...

    @post("/device/")
    async def create_device(
        self, body: ad.DeviceCreationRequest
    ) -> ad.Device | None: ...

    @get("/metric/{uuid}")
    async def get_metric(self, uuid: UUID) -> ad.Metric | None: ...

    @get("/metric?name={name}&unit={unit}")
    async def get_metric_by_name_and_unit(
        self, name: str, unit: str
    ) -> ad.ListResponse[ad.Metric] | None: ...

    @post("/metric/")
    async def create_metric(
        self, body: ad.MetricCreationRequest
    ) -> ad.Metric | None: ...

    @post("/aggregator/")
    async def create_aggregator(
        self, body: ad.AggregatorCreationRequest
    ) -> ad.Aggregator | None: ...

    @put("/aggregator/{uuid}")
    async def update_aggregator(
        self, uuid: UUID, body: ad.Aggregator
    ) -> ad.Aggregator | None: ...

    @post("/snapshot")
    async def create_snapshot(self, body: ad.Snapshot) -> ad.Snapshot | None: ...
