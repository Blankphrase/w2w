# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0005_auto_20161116_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoviesList',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('page', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_pages', models.IntegerField(blank=True, null=True)),
                ('total_results', models.IntegerField(blank=True, null=True)),
                ('movies', models.ManyToManyField(related_name='+', to='tmdb.Movie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='movieslist',
            unique_together=set([('page',)]),
        ),
    ]
