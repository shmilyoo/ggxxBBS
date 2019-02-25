# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0056_auto_20150605_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('descr', models.CharField(default=b'', max_length=128, verbose_name='\u6295\u7968\u63cf\u8ff0')),
                ('is_multi', models.BooleanField(default=False, verbose_name='\u662f\u5426\u591a\u9009')),
                ('is_visible', models.BooleanField(default=False, verbose_name='\u662f\u5426\u56de\u590d\u53ef\u89c1')),
                ('max_choices', models.PositiveSmallIntegerField(default=1, verbose_name='\u6700\u5927\u53ef\u9009\u6570')),
                ('expiration', models.DateTimeField(auto_now_add=True, verbose_name='\u8fc7\u671f\u65f6\u95f4')),
                ('topic', models.ForeignKey(to='forum.Topic', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
                'db_table': 'poll',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('option', models.CharField(max_length=32, verbose_name='\u9009\u9879')),
                ('votes', models.PositiveSmallIntegerField(default=0, verbose_name='\u7968\u6570')),
                ('display_order', models.PositiveSmallIntegerField(default=0, verbose_name='\u6392\u5e8f')),
                ('voters', models.TextField(default=b'', verbose_name='\u6295\u7968\u7528\u6237\u5217\u8868')),
                ('poll', models.ForeignKey(to='forum.Poll', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False)),
            ],
            options={
                'db_table': 'poll_option',
            },
            bases=(models.Model,),
        ),
    ]
