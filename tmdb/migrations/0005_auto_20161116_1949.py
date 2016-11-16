# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0004_auto_20161116_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movieslist',
            name='movies',
        ),
        migrations.DeleteModel(
            name='MoviesList',
        ),
    ]
