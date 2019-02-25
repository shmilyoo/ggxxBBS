# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0053_remove_forum_last_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='last_post_time',
            field=models.DateTimeField(default=b'2000-01-01 00:00:00', verbose_name='\u6700\u540e\u53d1\u5e16/\u56de\u5e16\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='last_post_username',
            field=models.CharField(default=b'', max_length=16, verbose_name='\u6700\u540e\u53d1\u5e16/\u56de\u5e16\u7528\u6237\u540d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='last_topic_title',
            field=models.CharField(default=b'', max_length=128, verbose_name='\u6700\u540e\u4e3b\u9898\u6807\u9898'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='posts',
            field=models.IntegerField(default=0, verbose_name='\u56de\u8d34\u6570'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='today_posts',
            field=models.IntegerField(default=0, verbose_name='\u56de\u8d34\u6570'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='today_topics',
            field=models.IntegerField(default=0, verbose_name='\u4e3b\u9898\u8d34\u6570'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='topics',
            field=models.IntegerField(default=0, verbose_name='\u4e3b\u9898\u8d34\u6570'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='update_time',
            field=models.DateTimeField(default=b'2000-01-01 00:00:00', verbose_name='\u7edf\u8ba1\u65f6\u95f4'),
            preserve_default=True,
        ),
    ]
