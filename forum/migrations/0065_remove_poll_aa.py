# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0064_poll_aa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='aa',
        ),
    ]
