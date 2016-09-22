from reco.source import UserSource, JsonSource
from reco.exceptions import RecoSourceError
from reco.models import Reco, MovieSim
from accounts.models import MoviePref

import math
from functools import reduce


class Item2Item():

    def make_reco(self, source):
        pass


class SlopeOne():

    def make_reco(self, source):
        # base: [ { "id": <id>, "rating": <rating> } ]

        devs_agr = dict()
        reco_base = source.get_data()

        #1   ITERATE OVER ALL MOVIES IN THE USER'S PREFERENCES LIST (MOVIE_B)
        for movie in reco_base:
            #1.1 FOR EACH MOVIE B IDENTIFY ALL USERS WHO RATED THIS MOVIE
            if source.get_user().is_authenticated:
                movie_prefs = MoviePref.objects.values("preflist").exclude(
                    preflist=source.get_user().pref).filter(movie__id=movie["id"])
            else:
                movie_prefs = MoviePref.objects.values("preflist").filter(
                    movie__id=movie["id"])

            if len(movie_prefs) == 0:
                continue

            #1.2 FIND ALL NEW MOVIES (NOT RATED BY THE USER) WITHIN USERS' 
            #    PREFERENCES IDENTIFIED IN PREVIOUS STEP
            movies_pref = list(MoviePref.objects.values("movie__id", "rating")
                .filter(preflist__in = movie_prefs)
                .exclude(movie__id__in =\
                    [ item["id"] for item in reco_base if item["id"] != movie["id"]]
                )
            )

            #1.3 CALCULATE DEVIATIONS BETWEEN MOVIE B AND MOVIES IN 1.2
            pref_agr = dict()
            for pref in movies_pref:
                if pref["movie__id"] not in pref_agr:
                    pref_agr[pref["movie__id"]] = list()
                pref_agr[pref["movie__id"]].append(pref["rating"])

            movie_mean = sum(pref_agr[movie["id"]])/len(pref_agr[movie["id"]])
            for pref in pref_agr:
                if pref != movie["id"]:
                    if pref not in devs_agr:
                        devs_agr[pref] = list()
                    devs_agr[pref].append((
                        movie["rating"] + (
                            sum(pref_agr[pref])/len(pref_agr[pref]) - movie_mean
                        ), 
                        len(pref_agr[pref])
                    ))

        #2   AGGREGATE DEVIATIONS AND ESTIMATE RATINGS
        reco = list()
        for movie in devs_agr:
            temp = reduce(
                lambda x,y: (x[0]+y[0]*y[1],x[1]+y[1]), 
                devs_agr[movie], 
                (0, 0)
            )
            if temp[1] != 0:
                reco.append({"id": movie, "rating": temp[0]/temp[1], 
                    "freq": temp[1]})

        return reco


class RecoManager:

    def __init__(self, source, engine = None):
        self.source = source
        self.last_reco = None

        if engine is None:
            self.engine = globals()["SlopeOne"]()
        else:
            self.engine = engine


    def get_reco(self, user = None):
        reco = Reco.create_new(
            base = self.source.get_data(), 
            reco = self.make_reco(), 
            user = user
        )
        return reco


    def make_reco(self):
        if self.source.is_empty():
            raise RecoSourceError
        self.last_reco = self.engine.make_reco(self.source)
        return self.last_reco


    def save_last_reco(self):
        reco = Reco.create_new(
            base = self.source.get_data(), 
            reco = self.last_reco, 
            user = self.source.get_user()
        )
        return reco   


    @property
    def base(self):
        return self.source.get_data()