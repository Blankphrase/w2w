# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tmdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email address', unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_real', models.BooleanField(default=True)),
                ('mean_rating', models.FloatField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MoviePref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('rating', models.FloatField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('movie', models.ForeignKey(related_name='ratings', to='tmdb.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='PrefList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('movies', models.ManyToManyField(related_name='preflist', to='tmdb.Movie', through='accounts.MoviePref')),
                ('user', models.OneToOneField(related_name='pref', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('country', models.CharField(max_length=255, blank=True, null=True)),
                ('sex', models.CharField(max_length=1, blank=True, null=True, choices=[('M', 'Male'), ('F', 'Female')])),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('movies', models.ManyToManyField(related_name='watchlist+', to='tmdb.Movie')),
                ('user', models.OneToOneField(related_name='watchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='moviepref',
            name='preflist',
            field=models.ForeignKey(related_name='data', to='accounts.PrefList'),
        ),
    ]
