# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0069_auto_20150611_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='descr',
            field=models.CharField(default=b'', max_length=128, verbose_name='\u6295\u7968\u63cf\u8ff0'),
            preserve_default=True,
        ),
    ]
