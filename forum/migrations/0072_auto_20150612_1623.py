# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0071_auto_20150612_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='last_reply_name',
            field=models.CharField(default=b'', max_length=16, verbose_name='\u6700\u540e\u56de\u590d\u7528\u6237\u6635\u79f0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='last_reply_time',
            field=models.DateTimeField(default=b'2000-01-01 00:00:00', verbose_name='\u6700\u540e\u56de\u590d\u65f6\u95f4', auto_now=True),
            preserve_default=True,
        ),
    ]
