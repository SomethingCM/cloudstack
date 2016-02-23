# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('api_key', models.CharField(max_length=200, blank=True)),
                ('secretkey', models.CharField(max_length=200, blank=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u8868',
                'verbose_name_plural': '\u7528\u6237\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DateCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': '\u673a\u623f',
                'verbose_name_plural': '\u673a\u623f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=100, blank=True)),
                ('cpus', models.CharField(max_length=10, blank=True)),
                ('maxmem', models.CharField(max_length=10, blank=True)),
                ('status', models.CharField(max_length=10, blank=True)),
                ('machinename', models.CharField(max_length=100, blank=True)),
                ('machineid', models.CharField(max_length=200, blank=True)),
                ('templatename', models.CharField(max_length=100, blank=True)),
                ('ip', models.CharField(max_length=200, blank=True)),
                ('datecenter', models.ForeignKey(to='auto_cloud.DateCenter')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u673a\u5668\u8868',
                'verbose_name_plural': '\u673a\u5668\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('networkid', models.CharField(max_length=100, blank=True)),
                ('displaytext', models.CharField(max_length=200, blank=True)),
                ('datecenter', models.ForeignKey(to='auto_cloud.DateCenter')),
            ],
            options={
                'verbose_name': '\u7f51\u7edcID',
                'verbose_name_plural': '\u7f51\u7edcID',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('templateid', models.CharField(max_length=100, blank=True)),
                ('displaytext', models.CharField(max_length=200, blank=True)),
                ('ostypename', models.CharField(max_length=100, blank=True)),
                ('datecenter', models.ForeignKey(to='auto_cloud.DateCenter')),
            ],
            options={
                'verbose_name': '\u6a21\u677f\u8868',
                'verbose_name_plural': '\u6a21\u677f\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='datecenter',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='clouduser',
            name='datecenter',
            field=models.ForeignKey(to='auto_cloud.DateCenter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clouduser',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
