# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0103_notification_is_broadcast'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='is_broadcast',
        ),
    ]
