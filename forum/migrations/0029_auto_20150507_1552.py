# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0028_auto_20150507_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='last_topic_id',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='last_topic_time',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='last_topic_title',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='last_topic_user',
        ),
    ]
