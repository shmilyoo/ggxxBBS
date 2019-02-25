# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0074_auto_20150613_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='ip',
            field=models.GenericIPAddressField(protocol=b'IPv4', verbose_name='\u53d1\u5e16IP'),
            preserve_default=True,
        ),
    ]
