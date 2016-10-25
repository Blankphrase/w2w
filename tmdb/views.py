from django.http.response import HttpResponse, JsonResponse
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from tmdb.client import Client
from tmdb.settings import TMDB_MAX_PAGE, TMDB_MIN_PAGE

import re

@csrf_exempt
def nowplaying_movies(request):
    if request.method == "POST":
        page = int(request.POST.get("page", 1))
    else:
        page = int(request.GET.get("page", 1))
    data = Client().get_nowplaying_movies(page = page)
    return JsonResponse(data)

@csrf_exempt
def upcoming_movies(request):
    if request.method == "POST":
        page = int(request.POST.get("page", 1))
    else:
        page = int(request.GET.get("page", 1))
    data = Client().get_upcoming_movies(page = page)
    return JsonResponse(data)

@csrf_exempt
def toprated_movies(request):
    if request.method == "POST":
        page = int(request.POST.get("page", 1))
    else:
        page = int(request.GET.get("page", 1))
    data = Client().get_toprated_movies(page = page)
    return JsonResponse(data)

@csrf_exempt
def popular_movies(request):
    if request.method == "POST":
        page = int(request.POST.get("page", 1))
    else:
        page = int(request.GET.get("page", 1))
    data = Client().get_popular_movies(page = page)
    return JsonResponse(data)

@csrf_exempt
def search_movies(request):
    if request.method == "POST":
        page = int(request.POST.get("page", 1))
        query = request.POST.get("query", None)
    else:
        page = int(request.GET.get("page", 1))
        query = request.GET.get("query", None)

    if query:
        query = "+".join(re.findall(r"(\w+)", query))   
        
    data = Client().search_movies(query, page)
    return JsonResponse(data)