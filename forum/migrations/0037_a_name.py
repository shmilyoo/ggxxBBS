# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0036_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='a',
            name='name',
            field=models.CharField(default=b'', max_length=12),
            preserve_default=True,
        ),
    ]
