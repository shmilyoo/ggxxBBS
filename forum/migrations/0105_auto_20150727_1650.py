# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0104_remove_notification_is_broadcast'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='has_img',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u7cbe\u534e\u5e16'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='is_poll',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u56fe\u7247\u8d34'),
            preserve_default=True,
        ),
    ]
