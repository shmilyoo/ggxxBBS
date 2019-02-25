# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0019_auto_20150507_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='day_hits',
            field=models.PositiveIntegerField(default=0, verbose_name='\u65e5\u70b9\u51fb'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='is_poll',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u6295\u7968\u8d34'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='last_view',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0), verbose_name='\u6700\u540e\u8bbf\u95ee\u65f6\u95f4', auto_now=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='month_hits',
            field=models.PositiveIntegerField(default=0, verbose_name='\u6708\u70b9\u51fb'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='week_hits',
            field=models.PositiveIntegerField(default=0, verbose_name='\u5468\u70b9\u51fb'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='year_hits',
            field=models.PositiveIntegerField(default=0, verbose_name='\u5e74\u70b9\u51fb'),
            preserve_default=True,
        ),
    ]
