# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0008_auto_20161116_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviepopularquery',
            name='movies',
            field=models.ManyToManyField(related_name='tmdb_moviepopularquery_query+', to='tmdb.Movie'),
        ),
        migrations.AlterField(
            model_name='nowplayingquery',
            name='movies',
            field=models.ManyToManyField(related_name='tmdb_nowplayingquery_query+', to='tmdb.Movie'),
        ),
        migrations.AlterField(
            model_name='topratedquery',
            name='movies',
            field=models.ManyToManyField(related_name='tmdb_topratedquery_query+', to='tmdb.Movie'),
        ),
        migrations.AlterField(
            model_name='upcomingquery',
            name='movies',
            field=models.ManyToManyField(related_name='tmdb_upcomingquery_query+', to='tmdb.Movie'),
        ),
    ]
