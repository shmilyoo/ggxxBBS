# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_myuser_last_visit_ip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='level',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='read_level',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u9605\u8bfb\u6743\u9650'),
            preserve_default=True,
        ),
    ]
