# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20150401_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='icon',
            field=models.URLField(default=b'', verbose_name='\u56fe\u6807'),
            preserve_default=True,
        ),
    ]
