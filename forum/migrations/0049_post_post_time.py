# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0048_auto_20150526_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_time',
            field=models.DateTimeField(default=b'2000-01-01 00:00:00', verbose_name='\u56de\u5e16\u65f6\u95f4', auto_now_add=True),
            preserve_default=True,
        ),
    ]
