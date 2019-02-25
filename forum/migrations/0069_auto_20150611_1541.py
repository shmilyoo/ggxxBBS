# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0068_auto_20150611_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='descr',
            field=models.CharField(default=b'', max_length=128, verbose_name='\u6295\u7968\u63cf\u8ff0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='poll',
            name='expiry',
            field=models.CharField(default=b'', max_length=32, verbose_name='\u8fc7\u671f\u65f6\u95f4', blank=True),
            preserve_default=True,
        ),
    ]
