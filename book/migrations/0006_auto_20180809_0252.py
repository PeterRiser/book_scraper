# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-09 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20180809_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='upc',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
