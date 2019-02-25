# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_remove_forum_visible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='moderators',
        ),
    ]
