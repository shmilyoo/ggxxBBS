# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20150414_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_logout',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u767b\u51fa\u72b6\u6001'),
            preserve_default=True,
        ),
    ]
