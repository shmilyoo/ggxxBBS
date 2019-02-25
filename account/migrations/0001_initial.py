# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=16, verbose_name='\u7528\u6237\u540d')),
                ('nick_name', models.CharField(max_length=16, verbose_name='\u6635\u79f0')),
                ('email', models.EmailField(max_length=255, verbose_name='\u7535\u5b50\u90ae\u4ef6', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('is_admin', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7ba1\u7406\u5458')),
                ('gender', models.NullBooleanField(default=None, verbose_name='\u6027\u522b', choices=[(True, '\u7537'), (False, '\u5973'), (None, '\u4fdd\u5bc6')])),
                ('reg_ip', models.GenericIPAddressField(protocol=b'IPv4', verbose_name='\u6ce8\u518cIP')),
                ('reg_date', models.DateField(auto_now_add=True, verbose_name='\u6ce8\u518c\u65e5\u671f')),
                ('last_visit', models.DateTimeField(auto_now_add=True, verbose_name='\u6700\u540e\u8bbf\u95ee\u65f6\u95f4')),
                ('topic_num', models.IntegerField(default=0, verbose_name='\u4e3b\u9898\u6570')),
                ('post_num', models.IntegerField(default=0, verbose_name='\u56de\u590d\u6570')),
                ('digest_number', models.IntegerField(default=0, verbose_name='\u7cbe\u534e\u5e16\u6570')),
                ('credits', models.IntegerField(default=0, verbose_name='\u79ef\u5206')),
            ],
            options={
                'db_table': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdminGroup',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('type', models.CharField(default=b'', unique=True, max_length=16, verbose_name='\u7ba1\u7406\u7c7b\u578b')),
            ],
            options={
                'db_table': 'admin_group',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('user', models.OneToOneField(primary_key=True, db_column=b'user_id', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('avatar', models.ImageField(default=b'', upload_to=b'avatar', verbose_name='\u5934\u50cf')),
                ('avatarwidth', models.PositiveSmallIntegerField(default=60, verbose_name='\u5934\u50cf\u5bbd\u5ea6')),
                ('avatarheight', models.PositiveSmallIntegerField(default=60, verbose_name='\u5934\u50cf\u9ad8\u5ea6')),
                ('bio', models.CharField(default=b'', max_length=255, verbose_name='\u4e2a\u4eba\u7b80\u4ecb')),
                ('signature', models.CharField(default=b'', max_length=500, verbose_name='\u4e2a\u4eba\u7b7e\u540d')),
            ],
            options={
                'db_table': 'user_info',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', uuidfield.fields.UUIDField(primary_key=True, auto=True, serialize=False)),
                ('name', models.CharField(max_length=16)),
                ('level', models.PositiveSmallIntegerField(default=1, unique=True, verbose_name='\u7ea7\u522b')),
            ],
            options={
                'db_table': 'user_group',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='myuser',
            name='admin_group',
            field=models.ForeignKey(db_constraint=False, default=0, verbose_name='\u7ba1\u7406\u5458\u7ec4', to='account.AdminGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_group',
            field=models.ForeignKey(db_constraint=False, verbose_name='\u7528\u6237\u7ec4', to='account.UserGroup'),
            preserve_default=True,
        ),
    ]
