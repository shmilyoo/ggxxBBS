# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0040_auto_20150508_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='descr',
            field=ckeditor.fields.RichTextField(default=b'', verbose_name='\u7248\u5757\u7b80\u8981\u4ecb\u7ecd', blank=True),
            preserve_default=True,
        ),
    ]
