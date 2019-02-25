# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0042_auto_20150508_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='is_top_all',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5168\u7ad9\u7f6e\u9876'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='content',
            field=models.TextField(default=b'', verbose_name='\u7248\u5757\u8be6\u7ec6\u4ecb\u7ecd(\u663e\u793a\u5728\u6b64\u7248\u5757\u9875\u9762\u4e2d)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='descr',
            field=models.TextField(default=b'', verbose_name='\u7248\u5757\u7b80\u8981\u4ecb\u7ecd(\u663e\u793a\u5728\u7248\u5757\u5217\u8868\u4e2d)', blank=True),
            preserve_default=True,
        ),
    ]
