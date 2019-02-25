# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0033_auto_20150507_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('post', models.ForeignKey(to='forum.Post', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
                ('topic', models.ForeignKey(to='forum.Topic', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
                'db_table': 'attachment',
            },
            bases=(models.Model,),
        ),
    ]
