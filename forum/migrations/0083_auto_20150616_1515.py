# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0082_remove_post_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polloption',
            name='voters',
        ),
        migrations.AddField(
            model_name='poll',
            name='voters',
            field=models.TextField(default=b'', verbose_name='\u6295\u7968\u7528\u6237\u5217\u8868'),
            preserve_default=True,
        ),
    ]
