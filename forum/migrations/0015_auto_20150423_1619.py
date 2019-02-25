# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0014_auto_20150423_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(max_length=128, verbose_name='\u6807\u9898', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(max_length=128, verbose_name='\u6807\u9898', blank=True),
            preserve_default=True,
        ),
    ]
