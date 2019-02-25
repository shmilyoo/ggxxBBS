# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0097_auto_20150702_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='has_read',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u8bfb'),
            preserve_default=True,
        ),
    ]
