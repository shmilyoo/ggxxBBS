# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_auto_20150409_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderatorrelation',
            name='forum',
            field=models.ForeignKey(to='forum.Forum', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='moderatorrelation',
            name='moderator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False),
            preserve_default=True,
        ),
    ]
