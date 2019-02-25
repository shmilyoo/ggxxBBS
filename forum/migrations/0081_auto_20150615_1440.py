# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0080_auto_20150615_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='last_nickname',
            field=models.CharField(default=b'', max_length=16, verbose_name='\u6700\u540e\u53d1\u5e16/\u56de\u5e16\u7528\u6237\u6635\u79f0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='last_topic_id',
            field=models.CharField(default=b'', max_length=32, verbose_name='\u6700\u540e\u4e3b\u9898\u5e16ID'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='last_topic_title',
            field=models.CharField(default=b'', max_length=128, verbose_name='\u6700\u540e\u4e3b\u9898\u6807\u9898'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='last_username',
            field=models.CharField(default=b'', max_length=16, verbose_name='\u6700\u540e\u53d1\u5e16/\u56de\u5e16\u7528\u6237\u540d'),
            preserve_default=True,
        ),
    ]
