# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(related_name='recos', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecoBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('rating', models.IntegerField()),
                ('movie', models.ForeignKey(related_name='reco_base+', to='tmdb.Movie')),
                ('reco', models.ForeignKey(related_name='base', to='reco.Reco')),
            ],
        ),
        migrations.CreateModel(
            name='RecoMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('score', models.FloatField(blank=True, null=True)),
                ('movie', models.ForeignKey(related_name='reco_movie+', to='tmdb.Movie')),
                ('reco', models.ForeignKey(related_name='movies', to='reco.Reco')),
            ],
        ),
    ]
