# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20150326_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='level',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='icon',
            field=models.ImageField(default=b'', upload_to=b'userGroupIcon', verbose_name='\u56fe\u6807'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usergroup',
            name='need_credits',
            field=models.PositiveIntegerField(default=0, verbose_name='\u9700\u8981\u79ef\u5206'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='credits',
            field=models.PositiveIntegerField(default=0, verbose_name='\u79ef\u5206'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='digest_number',
            field=models.PositiveIntegerField(default=0, verbose_name='\u7cbe\u534e\u5e16\u6570'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='post_num',
            field=models.PositiveIntegerField(default=0, verbose_name='\u56de\u590d\u6570'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='topic_num',
            field=models.PositiveIntegerField(default=0, verbose_name='\u4e3b\u9898\u6570'),
            preserve_default=True,
        ),
    ]
