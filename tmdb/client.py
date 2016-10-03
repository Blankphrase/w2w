from tmdb.models import (
    Movie, MoviePopularQuery,
    MIN_UPDATE_LEVEL, MAX_UPDATE_LEVEL
)
from tmdb.util import tmdb_request
from tmdb.exceptions import MovieDoesNotExist

from django.forms import model_to_dict

import requests


class Client():
    
    def get_popular_movies(
        self, page = 1, update_data = False, min_update_level = 0
    ):
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
                total_results = data["total_results"]
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


    def get_movie(self, id, min_update_level = MIN_UPDATE_LEVEL):
        try:
            movie = Movie.objects.get(id = id)
            if movie.update_level < min_update_level:
                data = self._download_movie_data(id)
                data["update_level"] = MAX_UPDATE_LEVEL
                fields_to_update = [
                    field.name for field in Movie._meta.get_fields()\
                        if field.name != "id"
                ]
                Movie.objects.filter(id = id).update(**{
                    key: value for key, value in data.items()\
                        if key in fields_to_update
                    })       
        except Movie.DoesNotExist:
            data = self._download_movie_data(id)
            movie = self._save_movie_in_database(
                data, 
                update_level = MAX_UPDATE_LEVEL
            )
        return movie


    def _download_movie_data(self, id):
        data = tmdb_request(method = "GET", path = "movie/%s" % (id))
        if data.get("status_code", None) == 34:
            raise MovieDoesNotExist()
        return data


    def _save_movie_in_database(self, movie, update_level = None):
        movie = Movie.objects.create(
            id = movie["id"], 
            title = movie["title"],
            poster_path = movie.get("poster_path"),
            overview = movie.get("overview"),
            update_level = update_level
        )
        return movie


