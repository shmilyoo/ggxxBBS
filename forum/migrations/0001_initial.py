# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import uuidfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('parent_id', uuidfield.fields.UUIDField(default=b'00000000000000000000000000000000', verbose_name='\u7236\u7248\u5757')),
                ('belong', models.PositiveSmallIntegerField(default=0, verbose_name='\u6240\u5c5e\u8bba\u575b', choices=[(0, '\u5efa\u8a00\u732e\u7b56'), (1, '\u6280\u672f\u4ea4\u6d41')])),
                ('name', models.CharField(default=b'', max_length=64, verbose_name='\u7248\u5757\u540d\u79f0')),
                ('tag', models.CharField(default=b'', max_length=64, verbose_name='\u6807\u7b7e')),
                ('descr', models.TextField(default=b'', verbose_name='\u7248\u5757\u4ecb\u7ecd', blank=True)),
                ('path_list', models.CharField(default=b'', max_length=255, verbose_name='\u7248\u5757\u6240\u5904\u8def\u5f84')),
                ('visible', models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a')),
                ('display_order', models.PositiveSmallIntegerField(default=9999, verbose_name='\u663e\u793a\u987a\u5e8f')),
                ('topics', models.PositiveIntegerField(default=0, verbose_name='\u4e3b\u9898\u6570')),
                ('posts', models.PositiveIntegerField(default=0, verbose_name='\u56de\u5e16\u6570')),
                ('last_topic_id', uuidfield.fields.UUIDField(default=b'00000000000000000000000000000000', verbose_name='\u6700\u540e\u4e00\u4e2a\u4e3b\u9898\u5e16id')),
                ('last_topic_title', models.CharField(default=b'', max_length=255, verbose_name='\u6700\u540e\u4e3b\u9898\u5e16\u6807\u9898')),
                ('last_topic_time', models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0), verbose_name='\u6700\u540e\u4e3b\u9898\u5e16\u53d1\u8868\u65f6\u95f4')),
                ('last_topic_user', models.CharField(default=b'', max_length=16, verbose_name='\u6700\u540e\u53d1\u8868\u4e3b\u9898\u7528\u6237\u540d')),
                ('allow_topic', models.BooleanField(default=True, verbose_name='\u662f\u5426\u5141\u8bb8\u53d1\u5e16')),
                ('icon', models.ImageField(default=b'', upload_to=b'forumIcon', verbose_name='\u56fe\u6807')),
                ('topic_credit', models.PositiveSmallIntegerField(default=b'5', verbose_name='\u4e3b\u9898\u5e16\u79ef\u5206')),
                ('post_credit', models.PositiveSmallIntegerField(default=b'1', verbose_name='\u56de\u590d\u5e16\u79ef\u5206')),
                ('visit_level', models.PositiveSmallIntegerField(default=0, verbose_name='\u8bbf\u95ee\u7ea7\u522b')),
                ('topic_level', models.PositiveSmallIntegerField(default=1, verbose_name='\u8bbf\u95ee\u7ea7\u522b')),
                ('post_level', models.PositiveSmallIntegerField(default=1, verbose_name='\u8bbf\u95ee\u7ea7\u522b')),
                ('download_level', models.PositiveSmallIntegerField(default=0, verbose_name='\u8bbf\u95ee\u7ea7\u522b')),
                ('moderators', models.ManyToManyField(db_constraint=False, db_table=b'ModeratorRelation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['display_order'],
                'db_table': 'forum',
            },
            bases=(models.Model,),
        ),
    ]
