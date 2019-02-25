# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0077_auto_20150613_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='posts',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='today_posts',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='today_topics',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='topics',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='update_time',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='last_reply_name',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='last_reply_time',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='reply_num',
        ),
    ]
