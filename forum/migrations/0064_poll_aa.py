# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0063_auto_20150611_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='aa',
            field=models.DateTimeField(default=b'2000-01-01 00:00:00', verbose_name='aa', auto_now_add=True),
            preserve_default=True,
        ),
    ]
