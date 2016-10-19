# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-19 18:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0004_movie_update_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='NowPlayingQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_pages', models.IntegerField(blank=True, null=True)),
                ('total_results', models.IntegerField(blank=True, null=True)),
                ('movies', models.ManyToManyField(related_name='_nowplayingquery_movies_+', to='tmdb.Movie')),
            ],
        ),
        migrations.AlterField(
            model_name='moviepopularquery',
            name='movies',
            field=models.ManyToManyField(related_name='_moviepopularquery_movies_+', to='tmdb.Movie'),
        ),
        migrations.AlterUniqueTogether(
            name='nowplayingquery',
            unique_together=set([('page',)]),
        ),
    ]
