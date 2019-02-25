# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150310_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='belong',
            field=models.CharField(default=0, max_length=1, verbose_name='\u6240\u5c5e\u8bba\u575b', choices=[(b'0', '\u8bf7\u9009\u62e9\u8bba\u575b'), (b'1', '\u5efa\u8a00\u732e\u7b56'), (b'2', '\u6280\u672f\u4ea4\u6d41')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='download_level',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='\u4e0b\u8f7d\u9644\u4ef6\u7ea7\u522b'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='icon',
            field=models.ImageField(default=b'', upload_to=b'forumIcon', verbose_name='\u56fe\u6807', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='parent_id',
            field=uuidfield.fields.UUIDField(default=b'00000000000000000000000000000000', verbose_name='\u7236\u7248\u5757', name='parent_id', choices=[(b'00000000000000000000000000000000', '\u9996\u9875')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='post_level',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u56de\u5e16\u7ea7\u522b'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forum',
            name='topic_level',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u53d1\u5e16\u7ea7\u522b'),
            preserve_default=True,
        ),
    ]
