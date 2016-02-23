# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auto_cloud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceOfferings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serviceofferingid', models.CharField(max_length=100, blank=True)),
                ('displaytext', models.CharField(max_length=200, blank=True)),
                ('datecenter', models.ForeignKey(to='auto_cloud.DateCenter')),
            ],
            options={
                'verbose_name': '\u673a\u5668\u6a21\u677f',
                'verbose_name_plural': '\u673a\u5668\u6a21\u677f',
            },
            bases=(models.Model,),
        ),
    ]
