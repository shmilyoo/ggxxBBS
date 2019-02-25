# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0020_auto_20150507_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='last_post',
        ),
    ]
