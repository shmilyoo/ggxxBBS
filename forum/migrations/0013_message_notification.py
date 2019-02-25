# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0012_auto_20150414_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u9001\u65f6\u95f4')),
                ('content', models.CharField(default=b'', max_length=255, verbose_name='\u6d88\u606f\u5185\u5bb9')),
                ('from_user', models.ForeignKey(related_name='from_user', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, verbose_name='\u6e90\u7528\u6237', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name='to_user', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, verbose_name='\u76ee\u7684\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u9001\u65f6\u95f4')),
                ('content', models.CharField(default=b'', max_length=255, verbose_name='\u901a\u77e5\u5185\u5bb9')),
                ('to_user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='\u76ee\u7684\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notification',
            },
            bases=(models.Model,),
        ),
    ]
