# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0065_remove_poll_aa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='expiry',
            field=models.CharField(default=b'', max_length=32, verbose_name='\u8fc7\u671f\u65f6\u95f4'),
            preserve_default=True,
        ),
    ]
