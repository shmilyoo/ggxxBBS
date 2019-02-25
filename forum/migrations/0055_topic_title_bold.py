# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0054_auto_20150527_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='title_bold',
            field=models.BooleanField(default=False, verbose_name='\u6807\u9898\u662f\u5426\u52a0\u7c97'),
            preserve_default=True,
        ),
    ]
