# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0052_auto_20150527_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='last_topic',
        ),
    ]
