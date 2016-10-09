from tmdb.models import Movie

from django.db import models
from django.utils import timezone
from django.conf import settings
from reco.exceptions import SimCalculationError


class Reco(models.Model):
    
    base = models.ManyToManyField(Movie, through = "RecoBase", 
        related_name = "reco_base")
    movies = models.ManyToManyField(Movie, through = "RecoMovie",
        related_name = "reco_movies")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, null = True)

    timestamp = models.DateTimeField(default = timezone.now)

    @staticmethod
    def create_new(base, reco, user = None):
        reco_ = Reco.objects.create()

        obj2save = list()
        for item in base:
            base2reco = RecoBase(reco = reco_, rating = item["rating"])
            base2reco.movie_id = item["id"]
            obj2save.append(base2reco)
        RecoBase.objects.bulk_create(obj2save)

        obj2save = list()
        for item in reco:
            movie2reco = RecoMovie(reco = reco_, score = None)
            movie2reco.movie_id = item["id"]
        RecoMovie.objects.bulk_create(obj2save)

        if user and user.is_authenticated:
            user.reco_set.add(reco_)

        return reco_


class RecoBase(models.Model):
    reco = models.ForeignKey(Reco)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField()


class RecoMovie(models.Model):
    reco = models.ForeignKey(Reco)
    movie = models.ForeignKey(Movie)
    score = models.FloatField(blank=True,null=True)