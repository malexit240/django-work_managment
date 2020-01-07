from django.urls import path, re_path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from worker_managment.consumers import WorkConsumer

app = ProtocolTypeRouter({
    'websocket': URLRouter([
        re_path(r'',
                WorkConsumer, name='websocket'),
    ])
})
