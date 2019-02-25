# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0030_auto_20150507_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('post_id', models.ForeignKey(to='forum.Post', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='topic',
            name='is_hide',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u56de\u590d\u53ef\u89c1'),
            preserve_default=True,
        ),
    ]
