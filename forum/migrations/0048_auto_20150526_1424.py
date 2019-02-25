# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0047_remove_forum_download_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='post_level',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u5141\u8bb8\u56de\u5e16\u7684\u9605\u8bfb\u6743\u9650'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='topic_level',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u5141\u8bb8\u53d1\u5e16\u7684\u9605\u8bfb\u6743\u9650'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='visit_level',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='\u5141\u8bb8\u8bbf\u95ee\u7684\u9605\u8bfb\u6743\u9650'),
            preserve_default=True,
        ),
    ]
