# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0029_auto_20150507_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='is_locked',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u9501\u5b9a'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=models.TextField(default=b'', verbose_name='\u6b63\u6587', blank=True),
            preserve_default=True,
        ),
    ]
