# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reco', '0012_auto_20161015_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recobase',
            name='movie',
            field=models.ForeignKey(related_name='reco_base+', to='tmdb.Movie'),
        ),
        migrations.AlterField(
            model_name='recomovie',
            name='movie',
            field=models.ForeignKey(related_name='reco_movie+', to='tmdb.Movie'),
        ),
    ]
