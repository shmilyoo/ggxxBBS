# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20150413_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='user_group',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='\u7528\u6237\u7ec4', to='account.UserGroup'),
            preserve_default=True,
        ),
    ]
