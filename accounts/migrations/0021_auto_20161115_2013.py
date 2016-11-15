# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20161115_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='movies',
            field=models.ManyToManyField(related_name='watchlist+', to='tmdb.Movie'),
        ),
    ]
