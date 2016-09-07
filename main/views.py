from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from reco.source import UserSource, JsonSource
from reco.engine import RecoManager


def home_page(request):
    # Start with popular browsing mode
    request.session["browse_mode"] = "popular"
    request.session["browse_page"] = 1

    return render(request, "main/home.html")


def new_reco(request):
    reco_type = request.POST["reco-type"]

    if reco_type == "general":
        source = UserSource(user = request.user)
    elif reco_type == "standalone":
        source = JsonSource(preferences = request.POST["reco-pref"])

    rengine = RecoManager(source = source)

    # make_reco() will probably raise some errors in the future
    try:
        movies = rengine.make_reco()
    except Exception as e:
        raise e
        return JsonResponse({"status": "error", "info": ""})

    return JsonResponse({"status": "ok", "movies": movies}, safe=False) 