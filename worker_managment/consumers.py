"""this module contains consumers classes for websockets"""

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


def get_string_without_slashes(source: str):
    """returns a string without slash symbols"""
    return ''.join(source.split('/'))


class WorkConsumer(WebsocketConsumer):
    """this consumer is intends for websocket connaction for work(model) html page"""

    def connect(self):
        self.accept()

        self.group_name = get_string_without_slashes(self.scope['path'])

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)

    def page_reload(self, event):
        """asks clients to reload html page"""
        self.send(text_data='Resource was outdated. Please reload the page')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name)
