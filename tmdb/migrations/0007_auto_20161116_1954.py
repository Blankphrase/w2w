# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0006_auto_20161116_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='publications',
        ),
        migrations.AlterUniqueTogether(
            name='movieslist',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='movieslist',
            name='movies',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='MoviesList',
        ),
        migrations.DeleteModel(
            name='Publication',
        ),
    ]
