# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0037_a_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='A',
        ),
    ]
