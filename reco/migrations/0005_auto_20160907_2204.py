# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reco', '0004_auto_20160907_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reco',
            name='base',
            field=models.ManyToManyField(related_name='reco_base', through='reco.RecoBase', to='tmdb.Movie'),
        ),
        migrations.AlterField(
            model_name='reco',
            name='movies',
            field=models.ManyToManyField(related_name='reco_movies', through='reco.RecoMovie', to='tmdb.Movie'),
        ),
    ]