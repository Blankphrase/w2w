import requests

from django.forms import model_to_dict

from tmdb.models import (
    Movie, MoviePopularQuery, NowPlayingQuery, UpcomingQuery, TopRatedQuery,
    SEARCH_UPDATE_LEVEL, MIN_UPDATE_LEVEL
)
from tmdb.util import tmdb_request


class Client():

    def get_movies(self, cls, page, force_update):
        try:
            npq = cls.get(page = page, force_update = force_update)
            data = {
                "w2w_status": "OK",
                "movies": [ model_to_dict(movie,  
                    fields = [ "title", "id", "poster_path" ])\
                    for movie in npq.movies.all() ],
                "page": page,
                "total_pages": npq.total_pages,
                "total_results": npq.total_results
            }
        except requests.exceptions.RequestException:
            data = {"w2w_status": "ERROR" }

        return data      

    def get_nowplaying_movies(self, page, force_update = False):
        return self.get_movies(NowPlayingQuery, page, force_update)

    def get_popular_movies(self, page = 1, force_update = False):
        return self.get_movies(MoviePopularQuery, page, force_update)

    def get_toprated_movies(self, page = 1, force_update = False):
        return self.get_movies(TopRatedQuery, page, force_update)

    def get_upcoming_movies(self, page = 1, force_update = False):
        return self.get_movies(UpcomingQuery, page, force_update)
       
    def search_movies(self, query, page = 1):
        try:
            data = tmdb_request(method = "POST", path = "search/movie", 
                    params = {"page": page, "query": query})
            data["movies"] = data.pop("results", [])
            data["w2w_status"] = "OK"

            for movie in data["movies"]:
                try:
                    Movie.objects.get(
                        id = movie["id"], 
                        update_level__gte = SEARCH_UPDATE_LEVEL
                    )
                except:
                    movie["update_level"] = SEARCH_UPDATE_LEVEL
                    Movie.save_movie_in_db(id = movie["id"], data = movie)

        except requests.exceptions.RequestException:
            data = {"w2w_status": "ERROR"}
        
        return data

    def get_movie(self, id, min_update_level = MIN_UPDATE_LEVEL,
                  force_update = False):
        try:
            movie = Movie.get(id, min_update_level = min_update_level,
                              force_update = force_update)
            movie_fields = [
                field.name for field in Movie._meta.get_fields() 
                           if field.related_model is None 
            ]
            data = model_to_dict(movie, fields = movie_fields)
            data["genres"] = [
                {"id": genre.id, "name": genre.name} 
                for genre in movie.genres.all()
            ]
            data["w2w_status"] = "OK"
        except requests.exceptions.RequestException as e:
            data = {"w2w_status": "ERROR", 
                    "msg": "Connection error with TMDB."}
        except Movie.DoesNotExist:
            data = {"w2w_status": "ERROR", 
                    "msg": "Movie with given id does not exist."}

        return data