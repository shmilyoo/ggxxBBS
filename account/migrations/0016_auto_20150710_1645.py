# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20150608_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='bio',
            field=models.CharField(max_length=255, verbose_name='\u4e2a\u4eba\u7b80\u4ecb', blank=True),
            preserve_default=True,
        ),
    ]
