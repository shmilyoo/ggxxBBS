# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0073_topic_reply_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, default=b'00000000000000000000000000000000', verbose_name='\u53d1\u5e16\u4eba', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=b'', verbose_name='\u6b63\u6587', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='ip',
            field=models.GenericIPAddressField(default=b'0.0.0.0', protocol=b'IPv4', verbose_name='\u56de\u590dIP'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u9690\u85cf'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='last_edit_time',
            field=models.DateTimeField(default=b'2000-01-01 00:00:00', verbose_name='\u6700\u540e\u7f16\u8f91\u65f6\u95f4', auto_now=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='remark',
            field=models.CharField(default=b'', max_length=64, verbose_name='\u5907\u6ce8\u7f16\u8f91\u7ba1\u7406\u64cd\u4f5c'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default=b'', max_length=128, verbose_name='\u6807\u9898'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='ip',
            field=models.GenericIPAddressField(default=b'0.0.0.0', protocol=b'IPv4', verbose_name='\u53d1\u5e16IP'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='remark',
            field=models.CharField(default=b'', max_length=64, verbose_name='\u5907\u6ce8\u7f16\u8f91\u7ba1\u7406\u64cd\u4f5c'),
            preserve_default=True,
        ),
    ]
