from tmdb.models import Movie, MoviePopularQuery
from tmdb.util import tmdb_request


class Client:
    
    def get_popular_movies(self, page = 1, update_data = False):
        '''
        Returns MoviePopularQuery object for chosen page. First search internal
        database. When id doesn't exist, tries to load it from tmdb. 
        '''
        try:
            mpq = MoviePopularQuery.objects.get(page=page)
        except MoviePopularQuery.DoesNotExist:
            mpq = None

        if update_data or mpq is None:
            if mpq is not None:
                mpq.delete()

            response = tmdb_request(method = "GET", path = "movie/popular", 
                params = {"page": page})
            # Save query and movies in database
            mpq = MoviePopularQuery.objects.create(
                page = page,
                total_pages = response["total_pages"],
                total_results = response["total_results"],
            )
            for movie in response["results"]:
                try:
                    movie = Movie.objects.get(id = movie["id"])
                except Movie.DoesNotExist:
                    movie = self._save_movie_in_database(movie)
                mpq.movies.add(movie)

        return mpq

    def search_movies(self, query, page = 1):
        response = tmdb_request(method = "POST", path = "search/movie", 
                params = {"page": page, "query": query})

    def _save_movie_in_database(self, movie):
        movie = Movie(id = movie["id"], title = movie["title"])
        movie.full_clean()
        movie.save()
        return movie


