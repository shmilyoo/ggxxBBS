# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0049_post_post_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='post',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='posts',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='topics',
        ),
        migrations.AddField(
            model_name='topic',
            name='has_attachment',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u6709\u9644\u4ef6'),
            preserve_default=True,
        ),
    ]
