# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0062_auto_20150611_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='expiry',
            field=models.DateTimeField(default=b'2000-01-01 00:00:00', verbose_name='\u8fc7\u671f\u65f6\u95f4', auto_now_add=True),
            preserve_default=True,
        ),
    ]
