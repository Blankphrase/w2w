from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from reco.source import UserSource, JsonSource
from reco.engine import RecoManager, SlopeOne
from reco.settings import (
    RECO_MAX_MOVIES, RECO_MIN_FREQ, RECO_MIN_RATING
)
from tmdb.models import Movie
from accounts.models import PrefList


import json


def home_page(request):
    return render(request, "main/home.html")


def reco_page(request):
    # Start with popular browsing mode
    request.session["browse_mode"] = "popular"
    request.session["browse_page"] = 1

    reco_type = request.GET.get("type", "standalone")

    preflist = []
    if request.user.is_authenticated and reco_type == "general":
        preflist = list(request.user.pref.data.values(
            "movie__id", "movie__title", "rating"
        ).annotate(title=F("movie__title"), id=F("movie__id")).values(
            "id", "title", "rating"
        ).all())

    return render(request, "main/reco.html", {
        "preflist": json.dumps(preflist),
        "reco_type": reco_type
    })  


@csrf_exempt
def make_reco(request):
    reco_request = json.loads(request.body.decode())
    reco_type = reco_request["type"]

    if request.user.is_authenticated and reco_type == "general":
        source = UserSource(user = request.user)
    else:
        source = JsonSource(data = reco_request["prefs"], user = request.user)

    # Save pseudo preflist for anonymouse users. They can improve
    # recommendations for other users.
    if not request.user.is_authenticated:
        preflist = PrefList.objects.create()
        for movie in source.get_data():
            preflist.add(movie["id"], movie["rating"])

    rengine = RecoManager(source = source, engine = SlopeOne())
    reco = rengine.make_reco()

    if len(reco) > 0:
        reco_final = [ movie for movie in reco if movie["rating"] > RECO_MIN_RATING and
             movie["freq"] > RECO_MIN_FREQ ]
        reco_final = sorted(reco_final, key=lambda x: x["rating"], 
            reverse = True)
        reco_final = reco_final[0:min(len(reco_final), RECO_MAX_MOVIES)]

        reco_ids = [ movie["id"] for movie in reco_final ]
        movies = list(Movie.objects.values("id", "title")\
            .filter(id__in = reco_ids))
        movies = { movie["id"]: movie["title"] for movie in movies }

        for movie in reco_final:
            movie["title"] = movies.get(movie["id"])
            del movie["freq"]
    else:
        reco_final = []

    # substitute orginal reco with preparated by this view
    reco_db = rengine.save_reco(
        reco = reco_final
    ) 

    return JsonResponse({"status": "OK", "movies": reco_final, "id": 
        reco_db.id, "title": reco_db.title}, safe=False)