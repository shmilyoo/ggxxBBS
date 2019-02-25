# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20150714_0807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='digest_number',
        ),
    ]
