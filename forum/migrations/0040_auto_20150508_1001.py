# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0039_auto_20150508_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='icon',
            field=models.ImageField(upload_to=b'forumIcon', verbose_name='\u56fe\u6807', blank=True),
            preserve_default=True,
        ),
    ]
