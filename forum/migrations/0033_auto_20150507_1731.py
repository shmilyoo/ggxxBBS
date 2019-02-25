# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0032_auto_20150507_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='post_id',
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
    ]
