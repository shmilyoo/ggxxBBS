# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20150402_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='icon',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u56fe\u6807'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='name',
            field=models.CharField(max_length=16, verbose_name='\u540d\u79f0'),
            preserve_default=True,
        ),
    ]
