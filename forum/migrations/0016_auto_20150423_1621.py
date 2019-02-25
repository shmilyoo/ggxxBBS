# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0015_auto_20150423_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='title',
            field=models.CharField(default=b'', max_length=128, verbose_name='\u6807\u9898'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.CharField(default=b'', max_length=128, verbose_name='\u6807\u9898'),
            preserve_default=True,
        ),
    ]
