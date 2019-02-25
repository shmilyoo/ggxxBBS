# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0057_poll_polloption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='read_perm',
            new_name='read_level',
        ),
    ]
