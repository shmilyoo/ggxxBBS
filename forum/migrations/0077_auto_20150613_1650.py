# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0076_auto_20150613_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='against',
            field=models.PositiveIntegerField(default=0, verbose_name='\u53cd\u5bf9'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='support',
            field=models.PositiveIntegerField(default=0, verbose_name='\u652f\u6301'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='against',
            field=models.PositiveIntegerField(default=0, verbose_name='\u53cd\u5bf9'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='support',
            field=models.PositiveIntegerField(default=0, verbose_name='\u652f\u6301'),
            preserve_default=True,
        ),
    ]
