from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import asyncio
from time import sleep

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print("connection established....")
        print('channel Layer', self.channel_layer)  #get default channel layer from channel layer
        print('channel name', self.channel_name) #get channel name from channel
        #add channel to a group
        async_to_sync(self.channel_layer.group_add)('Programmers', self.channel_name)
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self, event):
        print(f"message received...  {event['text']}")

    def websocket_disconnect(self, event):
        print("connection closed...")
        print('channel Layer', self.channel_layer)  #get default channel layer from channel layer
        print('channel name', self.channel_name) #get channel name from channel
        async_to_sync(self.channel_layer.group.discard)('Programmers', self.channel_name)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connection established....")
        self.number = int(self.scope['url_route']['kwargs'].get('number'))
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self, event):
       print(f"message received...  {event['text']}")
       for i in range(1,11):
            await self.send({
                'type':'websocket.send',
                'text':f"{self.number} x {i} = {self.number * i}"
            })
            await asyncio.sleep(1)


    async def websocket_disconnect(self, event):
        print("connection closed...")
        raise StopConsumer()