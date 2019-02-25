# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0027_c'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='b',
            name='a',
        ),
        migrations.DeleteModel(
            name='A',
        ),
        migrations.DeleteModel(
            name='B',
        ),
        migrations.DeleteModel(
            name='C',
        ),
        migrations.AddField(
            model_name='topic',
            name='all_hits',
            field=models.PositiveIntegerField(default=0, verbose_name='\u603b\u70b9\u51fb'),
            preserve_default=True,
        ),
    ]
