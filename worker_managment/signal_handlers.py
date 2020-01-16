"""this module contains handlers for django signals"""

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import reverse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Work
from .consumers import get_string_without_slashes


@receiver(post_save, sender=Work)
def reload_work_page_callback(instance, **kwargs):
    """this callback function informs websocket clients that work(model) resource outdated and they must reload the page"""
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        get_string_without_slashes(
            reverse('wmanagment:works', kwargs={'pk': instance.company_id})), {'type': 'page.reload'})
