# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0018_topic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('name', models.CharField(default=b'', max_length=32, verbose_name='\u4e3b\u9898\u6807\u7b7e')),
                ('color', models.CharField(default='#000000', max_length=16, verbose_name='\u6807\u7b7e\u989c\u8272')),
                ('forum', models.ForeignKey(to='forum.Forum', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
                'db_table': 'subject',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together=set([('forum', 'name')]),
        ),
    ]
