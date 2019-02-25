# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20150518_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='nick_name',
            field=models.CharField(unique=True, max_length=16, verbose_name='\u6635\u79f0'),
            preserve_default=True,
        ),
    ]
