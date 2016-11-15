import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.template import Context
from django.template.loader import get_template

from reco.source import UserSource, JsonSource
from reco.engine import RecoManager, SlopeOne
from reco.settings import (
    RECO_MAX_MOVIES, RECO_MIN_FREQ, RECO_MIN_RATING
)
from tmdb.models import Movie
from accounts.models import PrefList


def about_page(request):
    return render(request, "main/about.html")

def home_page(request):
    if request.user.is_authenticated():
        reco = request.user.recos.order_by("-timestamp").first()
    else:
        reco = None
    return render(request, "main/home.html", { "reco": reco } )

def reco_page(request):
    reco_type = request.GET.get("type", "standalone")
    if reco_type != "general" and reco_type != "standalone":
        reco_type = "standalone"

    preflist = []
    if reco_type == "general":
        if not request.user.is_authenticated():
            return redirect("/")

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

    if request.user.is_authenticated() and reco_type == "general":
        source = UserSource(user = request.user)
    else:
        source = JsonSource(data = reco_request["prefs"], user = request.user)

    # Save pseudo preflist for anonymouse users. They can improve
    # recommendations for other users.
    if not request.user.is_authenticated():
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