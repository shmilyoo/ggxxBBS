# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20150319_1403'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='forum',
            index_together=set([]),
        ),
    ]
