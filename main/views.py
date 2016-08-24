from django.shortcuts import render
from django.http.request import HttpRequest

from tmdb.views import movie_popular
from tmdb.browse import PopularBrowseMode
import tmdb.browse as browse

import json

def home_page(request):

    browse_settings = dict()
    browse_settings["mode"] = request.session.get("browse_mode", "popular")
    browse_settings["page"] = request.session.get("browse_page", 1)
    
    if browse_settings["mode"] == "search":
        pass
        # request.session.get("browse_query")
        # request.session.get("browse_movies")
        # request.session.get("browse_movies_per_page")
        # request.session.get("browse_total_pages")

    movies = browse.get_movies(browse_settings)

    return render(request, "main/home.html",
        {"movies": movies}
    )