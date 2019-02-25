# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0045_auto_20150513_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='descr',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u7248\u5757\u7b80\u8981\u4ecb\u7ecd(\u663e\u793a\u5728\u7248\u5757\u5217\u8868\u4e2d)'),
            preserve_default=True,
        ),
    ]
