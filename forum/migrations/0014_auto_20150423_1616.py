# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0013_message_notification'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='message',
            table='message',
        ),
    ]
