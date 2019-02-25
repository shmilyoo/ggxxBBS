# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20150326_0845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='reg_date',
            new_name='reg_time',
        ),
    ]
