# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0061_auto_20150611_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='expiry',
            field=models.DateTimeField(default=b'2000-01-01 00:00:00', auto_now=True, auto_now_add=True, verbose_name='\u8fc7\u671f\u65f6\u95f4'),
            preserve_default=True,
        ),
    ]
