# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20150326_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='need_credits',
            field=models.PositiveIntegerField(default=0, unique=True, verbose_name='\u9700\u8981\u79ef\u5206'),
            preserve_default=True,
        ),
    ]
