# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150326_0845'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='info',
        #     name='user',
        # ),
        migrations.DeleteModel(
            name='Info',
        ),
    ]
