# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0060_auto_20150611_1026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='expiration',
            new_name='expiry',
        ),
    ]
