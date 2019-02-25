# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0058_auto_20150611_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='time',
        ),
    ]
