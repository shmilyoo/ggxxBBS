# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20150319_1405'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='forum',
            unique_together=set([('belong', 'tag'), ('belong', 'name')]),
        ),
    ]
