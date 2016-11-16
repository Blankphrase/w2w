# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('update_level', models.IntegerField(default=0)),
                ('title', models.TextField()),
                ('poster_path', models.TextField(blank=True, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('release_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.TextField(blank=True, null=True)),
                ('vote_count', models.IntegerField(blank=True, null=True)),
                ('vote_average', models.DecimalField(blank=True, max_digits=4, null=True, decimal_places=2)),
                ('popularity', models.DecimalField(blank=True, max_digits=4, null=True, decimal_places=2)),
                ('video', models.TextField(blank=True, null=True)),
                ('tagline', models.TextField(blank=True, null=True)),
                ('adult', models.NullBooleanField()),
                ('backdrop_path', models.TextField(blank=True, null=True)),
                ('budget', models.IntegerField(blank=True, null=True)),
                ('revenue', models.IntegerField(blank=True, null=True)),
                ('runtime', models.IntegerField(blank=True, null=True)),
                ('homepage', models.TextField(blank=True, null=True)),
                ('imdb_id', models.TextField(blank=True, null=True)),
                ('original_language', models.TextField(blank=True, null=True)),
                ('original_title', models.TextField(blank=True, null=True)),
                ('genres', models.ManyToManyField(related_name='movies', to='tmdb.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='MoviePopularQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('page', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_pages', models.IntegerField(blank=True, null=True)),
                ('total_results', models.IntegerField(blank=True, null=True)),
                ('movies', models.ManyToManyField(related_name='query+', to='tmdb.Movie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NowPlayingQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('page', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_pages', models.IntegerField(blank=True, null=True)),
                ('total_results', models.IntegerField(blank=True, null=True)),
                ('movies', models.ManyToManyField(related_name='query+', to='tmdb.Movie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TopRatedQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('page', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_pages', models.IntegerField(blank=True, null=True)),
                ('total_results', models.IntegerField(blank=True, null=True)),
                ('movies', models.ManyToManyField(related_name='query+', to='tmdb.Movie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UpcomingQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('page', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_pages', models.IntegerField(blank=True, null=True)),
                ('total_results', models.IntegerField(blank=True, null=True)),
                ('movies', models.ManyToManyField(related_name='query+', to='tmdb.Movie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='upcomingquery',
            unique_together=set([('page',)]),
        ),
        migrations.AlterUniqueTogether(
            name='topratedquery',
            unique_together=set([('page',)]),
        ),
        migrations.AlterUniqueTogether(
            name='nowplayingquery',
            unique_together=set([('page',)]),
        ),
        migrations.AlterUniqueTogether(
            name='moviepopularquery',
            unique_together=set([('page',)]),
        ),
    ]
