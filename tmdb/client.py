from tmdb.models import (
    Movie, MoviePopularQuery, NowPlayingQuery,
    MIN_UPDATE_LEVEL, MAX_UPDATE_LEVEL,
    POPULAR_UPDATE_LEVEL, SEARCH_UPDATE_LEVEL
)
from tmdb.util import tmdb_request
from tmdb.exceptions import MovieDoesNotExist

from django.forms import model_to_dict

import requests


class Client():
    

    def get_nowplaying_movies(self, page):

        try:
            NowPlayingQuery.objects.get(page = page)
        except:
            tmdb_request(method = "GET", path = "movie/nowplaying")
            NowPlayingQuery.objects.create(page = page)
            

    def get_popular_movies(self, page = 1, update_data = False):
        '''
        Returns popular movies for chosen page in dictionary form. First search 
        internal database. When id doesn't exist, tries to load it from tmdb. 
        '''
        try:
            mpq = MoviePopularQuery.objects.get(page=page)
        except MoviePopularQuery.DoesNotExist:
            mpq = None

        if mpq is not None and not update_data:
            # Some movies doesn't meet requirement of minimal update level. 
            # One can update all this movies one by one (very slow) or 
            # update them together kust like mpq doesn't exist or 
            # update_data flag is true 
            if mpq.movies.filter(update_level__lt = POPULAR_UPDATE_LEVEL).count() > 0:
                update_data = True
            else:
                data = {
                    "movies": [ model_to_dict(movie,  
                        fields = [ "title", "id", "poster_path" ])\
                        for movie in mpq.movies.all() ],
                    "page": page,
                    "total_pages": mpq.total_pages,
                    "total_results": mpq.total_results
                }

        
        if mpq is None or update_data:
            if mpq is not None:
                mpq.delete()

            try:
                data = tmdb_request(method = "GET", path = "movie/popular", 
                    params = {"page": page})
                data["movies"] = data.pop("results", [])

                # Save query and movies in database
                mpq = MoviePopularQuery.objects.create(
                    page = page,
                    total_pages = data["total_pages"],
                    total_results = data["total_results"]
                )

                # Filter already updated movies
                updated_movies = Movie.objects\
                    .filter(id__in=[ int(movie["id"]) for movie in data["movies"] ])\
                    .filter(update_level__gte=POPULAR_UPDATE_LEVEL)
                for movie in updated_movies:
                    mpq.movies.add(movie)
                updated_movies = [ movie.id for movie in updated_movies ]

                # Update not updated movies
                for movie in data["movies"]:
                    if movie["id"] not in updated_movies:
                        movie_db = self.save_or_update_movie_in_db(
                            data = movie,
                            update_level = POPULAR_UPDATE_LEVEL
                        )
                        mpq.movies.add(movie_db)

            except requests.exceptions.HTTPError:
                data = {"page": 1, "total_pages": 1, "movies": [], 
                    "total_results": 0}
            
        return data


    def search_movies(self, query, page = 1):
        '''
        Returns found movies in accordance with tmdb search engine.
        '''
        try:
            data = tmdb_request(method = "POST", path = "search/movie", 
                    params = {"page": page, "query": query})
            data["movies"] = data.pop("results", [])
            for movie in data["movies"]:
                self.save_or_update_movie_in_db(
                    data = movie,
                    update_level = POPULAR_UPDATE_LEVEL
                )
        except requests.exceptions.HTTPError:
            data = {
                "page": 1, "total_pages": 1, 
                "movies": [], "total_results": 0
            }
        
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
            movie = self.save_movie_in_db(
                data, 
                update_level = MAX_UPDATE_LEVEL
            )
        return movie

    
    def save_movie_in_db(self, data, update_level):
        movie = Movie.objects.create(
            id = data["id"], 
            title = data.get("title"),
            poster_path = data.get("poster_path"),
            overview = data.get("overview"),
            update_level = update_level
        )
        return movie


    def update_movie_in_db(self, data, update_level):
        data["update_level"] = update_level
        fields_to_update = [
            field.name for field in Movie._meta.get_fields()\
                if field.name != "id" and field.name in data
        ]       
        Movie.objects.filter(id = data["id"]).update(**{
            key: value for key, value in data.items()\
                if key in fields_to_update
        })      
    
     
    def save_or_update_movie_in_db(self, data, update_level):
        try:
            movie_db = Movie.objects.get(id = data["id"])
            if movie_db.update_level < update_level:
                self.update_movie_in_db(data, update_level)
        except Movie.DoesNotExist:
            movie_db = self.save_movie_in_db(data, update_level)
        return movie_db


    def _download_movie_data(self, id):
        data = tmdb_request(method = "GET", path = "movie/%s" % (id))
        if data.get("status_code", None) == 34:
            raise MovieDoesNotExist()
        return data