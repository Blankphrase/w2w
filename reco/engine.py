from .source import UserSource, JsonSource
from .exceptions import RecoSourceError
from .models import Reco, MovieSim

import math


class Item2Item():

    # def __init__(self, threshold):
    #     pass
    
    def make_reco(self, base):

        for movie in base

            MovieSim.objects.get(movie_base = movie["id"]).order_by("value").limit(10)

        pass
        # 1. Find movies similar to movies in base
        # 2. Sort them with respect to similarity measures
        # 3. Reommend the n most similar movies

    def pred_rating(self, movie):
        pass


class RecoManager:

    def __init__(self, source, engine = None):
        self.source = source

        if engine is None:
            self.engine = globals()["Item2Item"]()
        else:
            self.engine = engine

    def get_reco(self, user = None):
        if self.source.is_empty():
            raise RecoSourceError

        reco = Reco.create_new(
            base = self.source.get_data(), 
            reco = self.make_reco(), 
            user = user
        )
        return reco

    def make_reco(self):
        return self.engine.make_reco(self.source.get_data())

    @property
    def base(self):
        return self.source.get_data()