# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0096_auto_20150702_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=models.TextField(verbose_name='\u6b63\u6587'),
            preserve_default=True,
        ),
    ]
