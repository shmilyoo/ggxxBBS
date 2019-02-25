# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0085_auto_20150623_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='against_names',
        ),
        migrations.RemoveField(
            model_name='post',
            name='support_names',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='against_names',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='support_names',
        ),
        migrations.AddField(
            model_name='post',
            name='vote_names',
            field=models.TextField(default=b'', verbose_name='\u652f\u6301\u548c\u53cd\u5bf9\u7528\u6237\u540d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='vote_names',
            field=models.TextField(default=b'', verbose_name='\u652f\u6301\u548c\u53cd\u5bf9\u7528\u6237\u540d'),
            preserve_default=True,
        ),
    ]
