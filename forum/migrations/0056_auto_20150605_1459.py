# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0055_topic_title_bold'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachment',
            old_name='download_perm',
            new_name='read_level',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='description',
        ),
    ]
