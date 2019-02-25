# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20150319_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='content',
            field=models.TextField(default=b'', verbose_name='\u7248\u5757\u8be6\u7ec6\u4ecb\u7ecd', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='descr',
            field=models.TextField(default=b'', verbose_name='\u7248\u5757\u7b80\u8981\u4ecb\u7ecd', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='icon',
            field=models.ImageField(upload_to=b'forumIcon', verbose_name='\u56fe\u6807', blank=True),
            preserve_default=True,
        ),
    ]
