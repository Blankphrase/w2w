from tmdb.models import Movie, MoviePopularQuery
from tmdb.util import tmdb_request

from django.forms import model_to_dict

import requests


class Client:
    
    def get_popular_movies(self, page = 1, update_data = False):
        '''
        Returns popular movies for chosen page in dictionary form. First search 
        internal database. When id doesn't exist, tries to load it from tmdb. 
        '''
        try:
            mpq = MoviePopularQuery.objects.get(page=page)
            data = {
                "movies": [ model_to_dict(movie,  fields = [ "title", "id", "poster_path" ]) 
                    for movie in mpq.movies.all() ],
                "page": page,
                "total_pages": mpq.total_pages,
                "total_results": mpq.total_results
            }
        except MoviePopularQuery.DoesNotExist:
            mpq = None

        if update_data or mpq is None:
            if mpq is not None:
                mpq.delete()

            try:
                data = tmdb_request(method = "GET", path = "movie/popular", 
                    params = {"page": page})
                data["movies"] = data.pop("results", [])
            except requests.exceptions.HTTPError:
                data = {"page": 1, "total_pages": 1, "movies": [], 
                    "total_results": 0}
            
            # Save query and movies in database
            mpq = MoviePopularQuery.objects.create(
                page = page,
                total_pages = data["total_pages"],
                total_results = data["total_results"],
            )
            for movie in data["movies"]:
                try:
                    movie = Movie.objects.get(id = movie["id"])
                except Movie.DoesNotExist:
                    movie = self._save_movie_in_database(movie)
                mpq.movies.add(movie)

        return data

    def search_movies(self, query, page = 1):
        try:
            data = tmdb_request(method = "POST", path = "search/movie", 
                    params = {"page": page, "query": query})
            data["movies"] = data.pop("results", [])
        except requests.exceptions.HTTPError:
            data = {"page": 1, "total_pages": 1, "movies": [],
                "total_results": 0}
        
        for movie in data["movies"]:
            if not Movie.objects.filter(id = movie["id"]).exists():
                movie = self._save_movie_in_database(movie)
        return data

    def _save_movie_in_database(self, movie):
        movie = Movie(id = movie["id"], title = movie["title"])
        movie.full_clean()
        movie.save()
        return movie


