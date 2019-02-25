# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0078_auto_20150613_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='last_post_time',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='last_post_username',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='last_topic_title',
        ),
    ]
