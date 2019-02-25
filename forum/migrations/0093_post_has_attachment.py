# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0092_auto_20150625_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='has_attachment',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u6709\u9644\u4ef6'),
            preserve_default=True,
        ),
    ]
