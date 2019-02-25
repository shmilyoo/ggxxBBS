# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='moderators',
            field=models.ManyToManyField(db_constraint=False, db_table=b'moderator_relation', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
