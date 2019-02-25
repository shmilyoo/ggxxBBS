# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0072_auto_20150612_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='reply_num',
            field=models.PositiveIntegerField(default=0, verbose_name='\u56de\u590d\u6570'),
            preserve_default=True,
        ),
    ]
