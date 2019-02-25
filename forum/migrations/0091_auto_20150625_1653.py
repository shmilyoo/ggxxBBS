# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0090_auto_20150625_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='topic',
        ),
        migrations.AddField(
            model_name='attachment',
            name='tp_id',
            field=models.CharField(default=b'', max_length=32, verbose_name='post\u6216topic\u7684id'),
            preserve_default=True,
        ),
    ]
