# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0079_auto_20150614_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='today_posts',
            field=models.PositiveSmallIntegerField(default=b'0', verbose_name='\u4eca\u65e5\u53d1\u5e16'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='update_time',
            field=models.DateTimeField(default=b'2000-01-01 00:00:00', verbose_name='\u4eca\u65e5\u53d1\u5e16\u7edf\u8ba1\u65f6\u95f4'),
            preserve_default=True,
        ),
    ]
