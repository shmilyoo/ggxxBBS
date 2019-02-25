# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20150316_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='parent_id',
            field=uuidfield.fields.UUIDField(default=b'00000000000000000000000000000000', verbose_name='\u7236\u7248\u5757', name='parent_id'),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='forum',
            index_together=set([('belong', 'tag'), ('belong', 'name')]),
        ),
    ]
