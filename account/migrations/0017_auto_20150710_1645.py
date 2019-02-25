# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20150710_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='signature',
            field=models.CharField(max_length=500, verbose_name='\u4e2a\u4eba\u7b7e\u540d', blank=True),
            preserve_default=True,
        ),
    ]
