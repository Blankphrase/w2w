from tmdb.models import Movie

from django.db import models
from django.utils import timezone
from django.conf import settings
from reco.exceptions import SimCalculationError
from django.shortcuts import reverse


class Reco(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, 
        null = True, related_name = "recos")

    timestamp = models.DateTimeField(default = timezone.now)
    title = models.TextField(blank = True, null = True)

    def get_absolute_url(self):
        return reverse("accounts:reco", args=[self.id])

    @staticmethod
    def create_new(base, reco, user = None, title = None):
        reco_ = Reco.objects.create(title = title)

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
            obj2save.append(movie2reco)
        RecoMovie.objects.bulk_create(obj2save)

        if user and user.is_authenticated():
            user.recos.add(reco_)

        return reco_


class RecoBase(models.Model):
    reco = models.ForeignKey(Reco, related_name = "base")
    movie = models.ForeignKey(Movie, related_name = "+")
    rating = models.IntegerField()


class RecoMovie(models.Model):
    reco = models.ForeignKey(Reco, related_name = "movies")
    movie = models.ForeignKey(Movie, related_name = "+")
    score = models.FloatField(blank=True,null=True)