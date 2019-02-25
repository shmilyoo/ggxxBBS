# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0043_auto_20150513_1003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='views',
        ),
    ]
