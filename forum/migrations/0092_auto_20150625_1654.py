# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0091_auto_20150625_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='tp_id',
            field=models.CharField(max_length=32, verbose_name='post\u6216topic\u7684id'),
            preserve_default=True,
        ),
    ]
