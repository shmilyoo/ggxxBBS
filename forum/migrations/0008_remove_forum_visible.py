# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20150324_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='visible',
        ),
    ]
