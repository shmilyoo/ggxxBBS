# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_usergroup_can_ip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='post_num',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='topic_num',
        ),
    ]
