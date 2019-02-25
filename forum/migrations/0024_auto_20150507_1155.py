# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0023_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(verbose_name='\u4e3b\u9898\u5e16', to='forum.Topic'),
            preserve_default=True,
        ),
    ]
