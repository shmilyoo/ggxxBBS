# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0067_auto_20150611_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(default=b'', max_length=128, verbose_name='\u6807\u9898'),
            preserve_default=True,
        ),
    ]
