# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0095_post_prefix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='prefix',
            field=models.TextField(default=b'', verbose_name='\u56de\u590d\u524d\u7f00'),
            preserve_default=True,
        ),
    ]
