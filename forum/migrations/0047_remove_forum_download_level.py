# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0046_auto_20150514_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='download_level',
        ),
    ]
