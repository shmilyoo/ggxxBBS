# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_usergroup_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='last_visit_ip',
            field=models.GenericIPAddressField(default=b'0.0.0.0', protocol=b'IPv4', verbose_name='\u6700\u540e\u8bbf\u95eeIP'),
            preserve_default=True,
        ),
    ]
