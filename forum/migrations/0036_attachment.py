# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0035_auto_20150507_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('file', models.FileField(upload_to=b'attachment', verbose_name='\u9644\u4ef6\u6587\u4ef6')),
                ('file_name', models.CharField(default=b'', max_length=64, verbose_name='\u9644\u4ef6\u540d\u79f0')),
                ('file_type', models.CharField(default=b'', max_length=16, verbose_name='\u6587\u4ef6\u7c7b\u578b')),
                ('file_size', models.PositiveIntegerField(default=0, verbose_name='\u6587\u4ef6\u5927\u5c0f(\u5b57\u8282)')),
                ('downloads', models.PositiveIntegerField(default=0, verbose_name='\u4e0b\u8f7d\u6b21\u6570')),
                ('description', models.CharField(default=b'', max_length=255, verbose_name='\u6587\u4ef6\u63cf\u8ff0')),
                ('download_perm', models.PositiveSmallIntegerField(default=0, verbose_name='\u9605\u8bfb\u6743\u9650')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='\u9644\u4ef6\u4e0a\u4f20\u65f6\u95f4')),
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
