# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_myuser_is_logout'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='level',
            field=models.PositiveSmallIntegerField(default=1, unique=True, verbose_name='\u7528\u6237\u7ec4\u7ea7\u522b'),
            preserve_default=True,
        ),
    ]
