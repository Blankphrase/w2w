# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0003_movieslist'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieslist',
            name='page',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movieslist',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='movieslist',
            name='total_pages',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movieslist',
            name='total_results',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='moviepopularquery',
            name='movies',
            field=models.ManyToManyField(to='tmdb.Movie', related_name='+'),
        ),
        migrations.AlterField(
            model_name='nowplayingquery',
            name='movies',
            field=models.ManyToManyField(to='tmdb.Movie', related_name='+'),
        ),
        migrations.AlterField(
            model_name='topratedquery',
            name='movies',
            field=models.ManyToManyField(to='tmdb.Movie', related_name='+'),
        ),
        migrations.AlterField(
            model_name='upcomingquery',
            name='movies',
            field=models.ManyToManyField(to='tmdb.Movie', related_name='+'),
        ),
    ]
