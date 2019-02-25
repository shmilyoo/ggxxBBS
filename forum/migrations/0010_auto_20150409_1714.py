# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0009_remove_forum_moderators'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeratorRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forum', models.ForeignKey(to='forum.Forum', db_constraint=False)),
                ('moderator', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_constraint=False)),
            ],
            options={
                'db_table': 'moderator_relation',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='moderatorrelation',
            unique_together=set([('forum', 'moderator')]),
        ),
    ]
