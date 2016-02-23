# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auto_cloud', '0002_serviceofferings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='serviceofferings',
            options={'verbose_name': '\u786c\u4ef6\u914d\u7f6e\u6a21\u677f', 'verbose_name_plural': '\u786c\u4ef6\u914d\u7f6e\u6a21\u677f'},
        ),
        migrations.AlterModelOptions(
            name='template',
            options={'verbose_name': '\u7cfb\u7edf\u6a21\u677f\u8868', 'verbose_name_plural': '\u7cfb\u7edf\u6a21\u677f\u8868'},
        ),
    ]
