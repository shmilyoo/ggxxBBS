# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0031_auto_20150507_1727'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='attachment',
            table='attachment',
        ),
    ]
