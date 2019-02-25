# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0050_auto_20150526_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='last_topic',
            field=models.ForeignKey(related_name='last_topic', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, default=b'00000000000000000000000000000000', to='forum.Topic'),
            preserve_default=True,
        ),
    ]
