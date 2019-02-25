# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0075_auto_20150613_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='\u53d1\u5e16\u4eba', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='ip',
            field=models.GenericIPAddressField(default=b'0.0.0.0', protocol=b'IPv4', verbose_name='\u53d1\u5e16IP'),
            preserve_default=True,
        ),
    ]
