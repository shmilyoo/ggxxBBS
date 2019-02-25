# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0025_auto_20150507_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='A',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='B',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default=b'', max_length=16)),
                ('a', models.ForeignKey(to='forum.A', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
