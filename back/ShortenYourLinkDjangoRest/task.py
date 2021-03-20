from __future__ import absolute_import, unicode_literals

import os
from datetime import datetime
from celery import shared_task
from django import setup

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'ShortenYourLinkDjangoRest.settings'
)
setup()

from ShortenYourLink.models import Link


@shared_task(name="test", type="test", ignore_result=True)
def test():
    dead_links = []
    for link in Link.objects.all():
        if link.life_time_end < datetime.utcnow():
            dead_links.append(link)
    if dead_links:
        for link in dead_links:
            link.delete()
        return "Links deleted successful"

    else:
        return "No links to delete"
