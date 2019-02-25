# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0093_post_has_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6536\u85cf\u65f6\u95f4')),
                ('topic', models.ForeignKey(to='forum.Topic', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
                'db_table': 'favorite',
            },
            bases=(models.Model,),
        ),
    ]
