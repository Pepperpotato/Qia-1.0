# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-07-10 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0013_auto_20190710_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcarttwentyfour',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='shopcarttwentyfour',
            name='totalprice',
            field=models.IntegerField(),
        ),
    ]
