from django.shortcuts import render
from django.http.request import HttpRequest

from tmdb.views import movie_popular

import json

def home_page(request):
    tmdb_request = HttpRequest()
    tmdb_request.method = "POST"
    tmdb_request.POST["page"] = 1
    movies = json.loads(movie_popular(tmdb_request).content.decode())["results"]

    # movies = tmdb_request("GET", "movie/popular").get("results")
    return render(request, "main/home.html",
        {"movies": movies}
    )