# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0094_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='prefix',
            field=models.CharField(default=b'', max_length=64, verbose_name='\u56de\u590d\u524d\u7f00'),
            preserve_default=True,
        ),
    ]
