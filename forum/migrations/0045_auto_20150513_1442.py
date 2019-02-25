# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0044_remove_topic_views'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='color',
            new_name='title_color',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='replies',
        ),
        migrations.AddField(
            model_name='topic',
            name='subject',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, default=b'00000000000000000000000000000000', verbose_name='\u5e16\u5b50\u4e3b\u9898', to='forum.Subject'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='is_digest',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u7cbe\u534e\u5e16'),
            preserve_default=True,
        ),
    ]
