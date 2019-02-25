# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0087_auto_20150625_0909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachment',
            old_name='read_level',
            new_name='download_level',
        ),
    ]
