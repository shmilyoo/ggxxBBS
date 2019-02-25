# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0041_auto_20150508_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='descr',
            field=models.TextField(default=b'', verbose_name='\u7248\u5757\u7b80\u8981\u4ecb\u7ecd', blank=True),
            preserve_default=True,
        ),
    ]
