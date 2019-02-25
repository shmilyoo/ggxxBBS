# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0100_auto_20150707_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='show_at_from',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a\u5728\u53d1\u4ef6\u4eba\u7684\u5df2\u53d1\u90ae\u4ef6\u4e2d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='show_at_to',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a\u5728\u6536\u4ef6\u4eba\u7684\u6536\u5230\u90ae\u4ef6\u4e2d'),
            preserve_default=True,
        ),
    ]
