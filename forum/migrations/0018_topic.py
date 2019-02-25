# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0017_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('read_perm', models.PositiveSmallIntegerField(default=0, verbose_name='\u9605\u8bfb\u6743\u9650')),
                ('title', models.CharField(default=b'', max_length=128, verbose_name='\u6807\u9898')),
                ('color', models.CharField(default='#000000', max_length=16, verbose_name='\u6807\u9898\u989c\u8272')),
                ('post_time', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e16\u65f6\u95f4')),
                ('last_edit_time', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u7f16\u8f91\u65f6\u95f4')),
                ('views', models.PositiveSmallIntegerField(default=0, verbose_name='\u88ab\u67e5\u770b\u6b21\u6570')),
                ('replies', models.PositiveSmallIntegerField(default=0, verbose_name='\u88ab\u56de\u590d\u6b21\u6570')),
                ('is_visible', models.BooleanField(default=True, verbose_name='\u662f\u5426\u9690\u85cf')),
                ('is_top', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7f6e\u9876')),
                ('is_bottom', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e0b\u6c89')),
                ('is_digest', models.BooleanField(default=True, verbose_name='\u662f\u5426\u7cbe\u534e\u5e16')),
                ('content', models.CharField(default=b'', max_length=255, verbose_name='\u6d88\u606f\u5185\u5bb9')),
                ('author', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='\u53d1\u5e16\u4eba', to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='\u6240\u5c5e\u7248\u5757', to='forum.Forum')),
                ('last_post', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='\u6700\u540e\u56de\u5e16', to='forum.Post')),
            ],
            options={
                'db_table': 'topic',
            },
            bases=(models.Model,),
        ),
    ]
