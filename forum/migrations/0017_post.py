# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0016_auto_20150423_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
            ],
            options={
                'db_table': 'post',
            },
            bases=(models.Model,),
        ),
    ]
