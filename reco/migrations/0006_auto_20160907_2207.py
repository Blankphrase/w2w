# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reco', '0005_auto_20160907_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recomovie',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]