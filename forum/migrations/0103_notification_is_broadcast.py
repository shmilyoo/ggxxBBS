# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0102_notification_is_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_broadcast',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5e7f\u64ad'),
            preserve_default=True,
        ),
    ]
