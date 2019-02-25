# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0088_auto_20150625_0910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='tp_id',
        ),
        migrations.AddField(
            model_name='attachment',
            name='topic',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, default=b'', to='forum.Topic'),
            preserve_default=True,
        ),
    ]
