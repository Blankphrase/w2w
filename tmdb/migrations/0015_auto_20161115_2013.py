# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0014_auto_20161115_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviepopularquery',
            name='movies',
            field=models.ManyToManyField(related_name='query+', to='tmdb.Movie'),
        ),
        migrations.AlterField(
            model_name='nowplayingquery',
            name='movies',
            field=models.ManyToManyField(related_name='query+', to='tmdb.Movie'),
        ),
        migrations.AlterField(
            model_name='topratedquery',
            name='movies',
            field=models.ManyToManyField(related_name='query+', to='tmdb.Movie'),
        ),
        migrations.AlterField(
            model_name='upcomingquery',
            name='movies',
            field=models.ManyToManyField(related_name='query+', to='tmdb.Movie'),
        ),
    ]
