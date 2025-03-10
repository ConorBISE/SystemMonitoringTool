from uuid import UUID

from channels.generic.websocket import AsyncWebsocketConsumer


class ControlChannelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.aggregator_id = UUID(self.scope["url_route"]["kwargs"]["aggregator_id"])
        self.group_name = f"control_{self.aggregator_id}"

        if self.channel_layer is not None:
            await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self):
        if self.channel_layer is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def control_message(self, event):
        message = event["message"]
        await self.send(message)
