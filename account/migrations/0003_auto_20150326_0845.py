# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150325_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='info',
            name='avatarheight',
        ),
        migrations.RemoveField(
            model_name='info',
            name='avatarwidth',
        ),
        migrations.RemoveField(
            model_name='info',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='info',
            name='signature',
        ),
        migrations.AddField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(default=b'', upload_to=b'avatar', verbose_name='\u5934\u50cf'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='avatarheight',
            field=models.PositiveSmallIntegerField(default=60, verbose_name='\u5934\u50cf\u9ad8\u5ea6'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='avatarwidth',
            field=models.PositiveSmallIntegerField(default=60, verbose_name='\u5934\u50cf\u5bbd\u5ea6'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='bio',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u4e2a\u4eba\u7b80\u4ecb'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='signature',
            field=models.CharField(default=b'', max_length=500, verbose_name='\u4e2a\u4eba\u7b7e\u540d'),
            preserve_default=True,
        ),
    ]
