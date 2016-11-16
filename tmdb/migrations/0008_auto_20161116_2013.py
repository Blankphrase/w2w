# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0007_auto_20161116_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviepopularquery',
            name='movies',
            field=models.ManyToManyField(to='tmdb.Movie', related_name='tmdb_moviepopularquery_ownership'),
        ),
        migrations.AlterField(
            model_name='nowplayingquery',
            name='movies',
            field=models.ManyToManyField(to='tmdb.Movie', related_name='tmdb_nowplayingquery_ownership'),
        ),
        migrations.AlterField(
            model_name='topratedquery',
            name='movies',
            field=models.ManyToManyField(to='tmdb.Movie', related_name='tmdb_topratedquery_ownership'),
        ),
        migrations.AlterField(
            model_name='upcomingquery',
            name='movies',
            field=models.ManyToManyField(to='tmdb.Movie', related_name='tmdb_upcomingquery_ownership'),
        ),
    ]
