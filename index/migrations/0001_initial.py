# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('desc', models.CharField(max_length=30, null=True)),
                ('url', models.TextField()),
                ('method', models.CharField(max_length=10, null=True)),
                ('headers', models.TextField(null=True)),
                ('body', models.TextField(null=True)),
                ('checks', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('description', models.CharField(max_length=50, null=True)),
                ('cases', models.ManyToManyField(to='index.Cases')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('password', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
    ]
