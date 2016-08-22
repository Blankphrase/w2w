from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers

from .util import tmdb_request
from .models import MoviePopularQuery, Movie


def movie_popular(request):
    '''
    arguments: page, force, save
    '''

    path = "movie/popular"
    
    # The logic of view is the same regardless of request's method
    if request.method == "GET":
        page = request.GET.get("page", 1)
        force = request.GET.get("force", False) # force tmdb_request
        save = request.GET.get("save", True) # save to database
    elif request.method == "POST":
        page = request.POST.get("page", 1)
        force = request.POST.get("force", False)
        save = request.POST.get("save", True)

    movies = dict()
    if not force:
        mpq = MoviePopularQuery.objects.filter(page = page).first()
        if mpq:
            movies["results"] = [ { "title": movie.title, "tmdb_id": 
                movie.tmdb_id } for movie in mpq.movies.all() ]
            movies["source"] = "w2w"
            movies["page"] = page

    if force or not movies:

        # Always update MoviePopularQuery with tmdb_request
        mpq = MoviePopularQuery.objects.filter(page = page).first()
        if mpq:
            mpq.delete()
        mpq = MoviePopularQuery.objects.create(page = page, 
            timestamp = timezone.now())

        # Load data from tmdb
        movies = tmdb_request(method = "GET", path = path,
            params = {"page": page})
        movies["source"] = "tmdb"

        # Save new movies to database
        for movie in movies["results"]:
            movie2add = Movie.objects.create(title = movie["title"], 
                tmdb_id = movie["id"])
            mpq.movies.add(movie2add)

    return JsonResponse(movies)