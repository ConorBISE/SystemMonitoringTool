import logging
from typing import Callable, Dict
import urllib.parse

import aiohttp
from pydantic import ValidationError

import common.api_definitions as ad

from .config import CONFIG

logger = logging.getLogger(__name__)


class ControlChannelListener:
    def __init__(
        self,
        aggregator: ad.Aggregator,
        command_map: Dict[ad.ControlCommand, Callable[[ad.ControlMessage], None]],
    ):
        self.aggregator = aggregator
        self.url = urllib.parse.urljoin(CONFIG.server_url, f"/ws/{aggregator.uuid}/")
        self.command_map = command_map

    async def run(self):
        async with aiohttp.ClientSession() as client_session:
            async with client_session.ws_connect(self.url) as ws:
                async for message in ws:
                    if message.type != aiohttp.WSMsgType.TEXT:
                        continue

                    try:
                        message = ad.ControlMessage.model_validate_json(message.data)
                    except ValidationError as e:
                        logger.error(
                            "Received malformed control command; skipping: %s",
                            message.data,
                        )
                        continue

                    logger.debug("Received control command: %s", message)

                    if message.command in self.command_map:
                        self.command_map[message.command](message)
