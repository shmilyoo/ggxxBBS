# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0105_auto_20150727_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='has_img',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u56fe\u7247\u5e16'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='is_poll',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u6295\u7968\u8d34'),
            preserve_default=True,
        ),
    ]
