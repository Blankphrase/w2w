# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20161012_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='movies',
            field=models.ManyToManyField(related_name='+', to='tmdb.Movie'),
        ),
    ]
