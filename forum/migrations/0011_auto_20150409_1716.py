# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_auto_20150409_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderatorrelation',
            name='id',
            field=uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False, name='id'),
            preserve_default=True,
        ),
    ]
