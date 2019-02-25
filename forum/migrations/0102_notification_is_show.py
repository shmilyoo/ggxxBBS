# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0101_auto_20150709_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_show',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a'),
            preserve_default=True,
        ),
    ]
