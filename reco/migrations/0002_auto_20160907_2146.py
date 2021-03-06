# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-07 21:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0002_auto_20160907_2033'),
        ('reco', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecoBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tmdb.Movie')),
                ('reco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reco.Reco')),
            ],
        ),
        migrations.AddField(
            model_name='reco',
            name='movies',
            field=models.ManyToManyField(through='reco.RecoBase', to='tmdb.Movie'),
        ),
    ]
