from django.shortcuts import render
from django.http import JsonResponse

from .util import tmdb_request


def movie_popular(request):
    '''
    arguments: page, force
    '''

    path = "movie/popular"
    
    # The logic of view is the same regardless of request's method
    if request.method == "GET":
        page = request.GET.get("page", 1)
        force = request.GET.get("force", False)
    elif request.method == "POST":
        page = request.POST.get("page", 1)
        force = request.POST.get("force", False)

    movies = tmdb_request(method = "GET", path = path,
        params = {"page": page})
    movies["source"] = "tmdb"
    
    return JsonResponse(movies)