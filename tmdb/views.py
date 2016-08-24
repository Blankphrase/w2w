from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers
from django.forms import model_to_dict

from .util import tmdb_request
from .models import MoviePopularQuery, Movie


def movie_popular(request):
    '''
    arguments: page, force
    '''

    path = "movie/popular"
    
    # The logic of view is the same regardless of request's method
    if request.method == "GET":
        page = request.GET.get("page", 1)
        force = request.GET.get("force", False) # force tmdb_request
    elif request.method == "POST":
        page = request.POST.get("page", 1)
        force = request.POST.get("force", False)

    movies = dict()
    if not force:
        mpq = MoviePopularQuery.objects.filter(page = page).first()
        if mpq:
            movies["results"] = [ model_to_dict(movie,
                    fields = [ "title", "tmdb_id" ]
                ) for movie in mpq.movies.all() ]

            movies["source"] = "w2w"
            movies["page"] = mpq.page
            movies["total_pages"] = mpq.total_pages
            movies["total_results"] = mpq.total_results

    if force or not movies:

        # Load data from tmdb, change id to tmdb_id
        movies = tmdb_request(method = "GET", path = path,
            params = {"page": page})
        movies["source"] = "tmdb"
        for movie in movies["results"]:
            movie["tmdb_id"] = movie.pop("id")

        # Always update MoviePopularQuery with tmdb_request
        mpq = MoviePopularQuery.objects.filter(page = page).first()
        if mpq:
            mpq.delete()
        mpq = MoviePopularQuery.objects.create(page = page, 
            timestamp = timezone.now(), total_pages = movies["total_pages"],
            total_results = movies["total_results"])

        # Save new movies to database
        for movie in movies["results"]:
            movie2add = Movie.objects.create(title = movie["title"], 
                tmdb_id = movie["tmdb_id"])
            mpq.movies.add(movie2add)

    return JsonResponse(movies)