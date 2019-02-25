# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20150710_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='can_ip',
            field=models.BooleanField(default=False, verbose_name='\u67e5\u770bIP'),
            preserve_default=True,
        ),
    ]
