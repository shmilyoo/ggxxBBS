# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0089_auto_20150625_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='topic',
            field=models.ForeignKey(to='forum.Topic', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False),
            preserve_default=True,
        ),
    ]
