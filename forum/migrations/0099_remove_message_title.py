# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0098_message_has_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='title',
        ),
    ]
