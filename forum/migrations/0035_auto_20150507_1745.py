# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0034_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='A',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='post',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
    ]
