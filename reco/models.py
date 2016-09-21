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

        for item in base:
            movie = Movie.objects.get(id = item["id"])
            base2reco = RecoBase(reco = reco_, movie = movie, 
                rating = item["rating"])
            base2reco.save()

        for item in reco:
            movie = Movie.objects.get(id = item["id"])
            movie2reco = RecoMovie(reco = reco_, movie = movie,
                score = None)
            movie2reco.save()

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


class MovieSim(models.Model):
    base_movie = models.ForeignKey(Movie, db_index = True, related_name='+')
    sim_movie = models.ForeignKey(Movie, related_name='+')
    
    value = models.FloatField(blank = False)
    timestamp = models.DateTimeField(default = timezone.now)

    @staticmethod
    def create_new(base_movie, sim_movie, simfunc = None, 
        simvalue = None, save = True
    ):
        try:
            sim = MovieSim(
                base_movie = base_movie,
                sim_movie = sim_movie,
                value = simvalue if simvalue is not None else simfunc(base_movie, sim_movie)
            )
            if save:
                sim.save()
            return sim
        except SimCalculationError:
            return None