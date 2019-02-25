# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0022_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('topic', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='\u4e3b\u9898\u5e16', to='forum.Topic')),
            ],
            options={
                'db_table': 'post',
            },
            bases=(models.Model,),
        ),
    ]
