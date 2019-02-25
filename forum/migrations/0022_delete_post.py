# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0021_remove_topic_last_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
