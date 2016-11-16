# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0002_auto_20161116_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoviesList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('movies', models.ManyToManyField(to='tmdb.Movie', related_name='+')),
            ],
        ),
    ]
