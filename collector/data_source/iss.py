import logging
import aiohttp
from urllib.parse import urlencode
from datetime import timedelta, datetime

from typing import Dict, Iterable

from collector.data_source.device_metric_gatherer import DeviceMetricGatherer
import common.api_definitions as ad

logger = logging.getLogger(__name__)


class ISSDataStream:
    """
    A simple no-frills Lightstream client that connects to a public lightstreamer instance
    where NASA is pushing telemetry from the ISS.

    based on: https://lightstreamer.com/sdks/ls-generic-client/2.3.0/TLCP%20Specifications.pdf
    and: https://github.com/Lightstreamer/Lightstreamer-example-ISSLive-client-javascript
    """

    SERVER = "wss://push.lightstreamer.com/lightstreamer"
    ADAPTER_SET = "ISSLIVE"
    THIRD_PARTY_MAGIC_CID = "mgQkwtwdysogQz2BJ4Ji%20kOj2Bg"

    def __init__(self, subscriptions: Iterable[str] | None = None):
        self.sub_id = 1
        self.subscription_group_map: Dict[int, str] = {}
        self.initial_subscriptions = subscriptions

    async def run(self):
        # TODO: refactor this
        async with aiohttp.ClientSession() as client_session:
            async with client_session.ws_connect(
                self.SERVER, protocols=["TLCP-2.3.0.lightstreamer.com"]
            ) as ws:
                await self._lightstreamer_request(ws, "wsok", {})

                await self._lightstreamer_request(
                    ws,
                    "create_session",
                    {
                        "LS_adapter_set": self.ADAPTER_SET,
                        "LS_cid": self.THIRD_PARTY_MAGIC_CID,
                        "LS_send_sync": "false",
                        "LS_cause": "api",
                    },
                )

                if self.initial_subscriptions is not None:
                    for group in self.initial_subscriptions:
                        await self._lightstreamer_request(
                            ws,
                            "control",
                            {
                                "LS_reqId": "1",
                                "LS_op": "add",
                                "LS_subId": str(self.sub_id),
                                "LS_mode": "MERGE",
                                "LS_group": group,
                                "LS_schema": "TimeStamp Value",
                                "LS_snapshot": "true",
                                "LS_requested_max_frequency": "unlimited",
                                "LS_ack": "false",
                            },
                        )

                        self.subscription_group_map[self.sub_id] = group
                        self.sub_id += 1

                async for msg in ws:
                    if msg.type != aiohttp.WSMsgType.TEXT:
                        continue

                    for line in msg.data.splitlines():
                        if not line.startswith("U"):
                            continue

                        try:
                            _, subscription_id, _, fields = line.split(",")
                            group = self.subscription_group_map[int(subscription_id)]
                            timestamp, value = fields.split("|")

                            current_year = datetime.now().year - 1
                            timestamp = datetime(
                                current_year, 12, 31, 0, 0, 0
                            ) + timedelta(hours=float(timestamp))
                            value = float(value)

                            yield group, timestamp, value
                        except Exception as e:
                            logger.error(
                                "Failed to parse lightstream message: %s", line
                            )
                            logger.exception(e)

    async def _lightstreamer_request(
        self, ws: aiohttp.ClientWebSocketResponse, method: str, data: Dict[str, str]
    ):
        d = f"{method}\r\n{urlencode(data)}"
        await ws.send_str(d)


class ISSStatisticsGatherer(DeviceMetricGatherer):
    NAME = "ISS"

    async def init_metrics(self):
        self.METRICS_MAP = {
            "USLAB000059": await self.find_create_metric(
                ad.MetricCreationRequest(name="Cabin Temperature", unit="°C")
            ),
            "NODE3000009": await self.find_create_metric(
                ad.MetricCreationRequest(name="Clean Water Tank", unit="%")
            ),
        }

    async def run(self):
        async for group, timestamp, value in ISSDataStream(
            self.METRICS_MAP.keys()
        ).run():
            await self.queue.put(
                ad.MetricReading(
                    metric_id=self.METRICS_MAP[group].uuid,
                    value=value,
                    timestamp=timestamp,
                    device_id=(await self.device).uuid,
                )
            )
