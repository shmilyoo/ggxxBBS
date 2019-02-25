# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0086_auto_20150624_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='topic',
        ),
        migrations.AddField(
            model_name='attachment',
            name='tp_id',
            field=models.CharField(default=b'', max_length=32, verbose_name='\u4e3b\u9898\u5e16\u6216\u56de\u5e16\u7684ID'),
            preserve_default=True,
        ),
    ]
