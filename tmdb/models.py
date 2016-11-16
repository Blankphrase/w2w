from requests.exceptions import HTTPError, RequestException
import json

from django.db import models
from django.utils import timezone

from tmdb.util import tmdb_request


MIN_UPDATE_LEVEL = 0
# POPULAR_UPDATE_LEVEL = 1
SEARCH_UPDATE_LEVEL = 1
# NOWPLAYING_UPDATE_LEVEL = 1
QUERY_UPDATE_LEVEL = 1
INFO_UPDATE_LEVEL = 2
MOVIE_UPDATE_LEVEL = 2
# MAX_UPDATE_LEVEL = 2


class Genre(models.Model):
    '''
    Genre Model
    Fields: id, name
    '''
    id = models.IntegerField(primary_key = True)
    name = models.TextField(unique = True)

    def add_movie(self, id = None, movie = None):
        '''
        Add movie to genre.
        '''
        if bool(id) == bool(movie):
            if not id:
                raise RuntimeError("Arguments error: id and movie are empty")
            else:   
                raise RuntimeError("Ambiguity error: id and movie filled")
        if id:
            movie = Movie.objects.get(id = id)
        self.movies.add(movie)

    def remove_movie(self, id = None, movie = None):
        '''
        Removie movie from genre.
        '''
        if bool(id) == bool(movie):
            if not id:
                raise RuntimeError("Arguments error: id and movie are empty")
            else:   
                raise RuntimeError("Ambiguity error: id and movie filled")
        if id:
            self.movies.remove(id)
        else:
            self.movies.remove(movie)

    @staticmethod
    def update_genres():
        """
        Update all genres in database ata once. TMDB API enables to download
        all genres in one query. Returns number of updated records. Catches
        RequestException and returns 0.

        TMDB response: {"genres": [
            {"id": 28, "name": "Action"},
            {"id": 12, "name": "Adventure"},
            ...
        ]}
        """
        try:
            response = tmdb_request(method = "GET", path = "genre/movie/list")
            for data_genre in response["genres"]:
                data = { key: value for key, value in data_genre.items()  }
                genre, created = Genre.objects.update_or_create(
                    id = data["id"], defaults = data
                )   
            return len(response["genres"]) 
        except RequestException:
            return 0


class Movie(models.Model):
    id = models.IntegerField(primary_key = True)
    update_level = models.IntegerField(default = 0)
    title = models.TextField()
    poster_path = models.TextField(blank = True, null = True)
    overview = models.TextField(blank = True, null = True)
    release_date = models.DateTimeField(blank = True, null = True)
    status = models.TextField(blank = True, null = True)
    vote_count = models.IntegerField(blank = True, null = True)
    vote_average = models.DecimalField(blank = True, null = True, 
                                       decimal_places = 2, max_digits=4)
    popularity = models.DecimalField(blank = True, null = True, 
                                       decimal_places = 2, max_digits=4)
    video = models.TextField(blank = True, null = True)
    tagline = models.TextField(blank = True, null = True)
    adult = models.NullBooleanField()
    backdrop_path = models.TextField(blank = True, null = True)
    budget = models.IntegerField(blank = True, null = True)
    revenue = models.IntegerField(blank = True, null = True)
    runtime = models.IntegerField(blank = True, null = True)
    homepage = models.TextField(blank = True, null = True)
    imdb_id = models.TextField(blank = True, null = True)
    original_language = models.TextField(blank = True, null = True)
    original_title = models.TextField(blank = True, null = True)

    genres = models.ManyToManyField(Genre, related_name = "movies")

    def __str__(self):
        return self.title

    def add_to_genre(self, id = None, genre = None):
        if bool(id) == bool(genre):
            if not id:
                raise RuntimeError("Arguments error: id and genre are empty")
            else:   
                raise RuntimeError("Ambiguity error: id and genre filled")
        if id:
            genre = Genre.objects.get(id = id)
        self.genres.add(genre)

    def remove_from_genre(self, id = None, genre = None):
        if bool(id) == bool(genre):
            if not id:
                raise RuntimeError("Arguments error: id and genre are empty")
            else:   
                raise RuntimeError("Ambiguity error: id and genre filled")
        if id:
            self.genres.remove(id)
        else:
            self.genres.remove(genre)

    @staticmethod
    def download_movie(id):
        try:
            data = tmdb_request(method = "GET", path = "movie/%s" % (id))
            if data.get("status_code", None) == 34:
                raise Movie.DoesNotExist()
            data["update_level"] = MOVIE_UPDATE_LEVEL  
        except HTTPError as e:
            if e.response.status_code == 404:
                if json.loads(e.response.text)["status_code"] == 34:
                    raise Movie.DoesNotExist()
            raise e
        return data

    @staticmethod
    def create_movie(id, data = None):
        if data is None:
            data = Movie.download_movie(id)

        fields_to_update = [ field.name for field in Movie._meta.get_fields() 
                                        if field.name not in ("genres",) ]
        data = { key: value for key, value in data.items() 
                            if key in fields_to_update }

        movie = Movie(**data)
        movie.id = id

        # Update genres
        if "genres" in data:
            genres_ids = [genre["id"] for genre in data["genres"]]
            movie.genres.remove()
            movie.genres.add(*genres_ids)

        return movie      

    @staticmethod
    def save_movie_in_db(id, *, data = None):
        if data is None:
            data = Movie.download_movie(id)

        # Update movie
        fields_to_update = [ field.name for field in Movie._meta.get_fields() 
                                        if field.name not in ("genres",) ]
        data4update = { key: value for key, value in data.items() 
                                   if key in fields_to_update and value}
        movie, created = Movie.objects.update_or_create(
            id = id, defaults = data4update
        )    

        # Update genres
        if "genres" in data:
            genres_ids = [genre["id"] for genre in data["genres"]]
            movie.genres.remove()
            movie.genres.add(*genres_ids)

        return movie      

    @staticmethod
    def get(id, min_update_level = MIN_UPDATE_LEVEL, 
         offline = False, force_update = False
    ):
        try:
            if force_update:
                raise Movie.DoesNotExist()
            movie = Movie.objects.get(id = id, 
                update_level__gte = min_update_level
            )
        except Movie.DoesNotExist:
            if offline:
                raise Movie.DoesNotExist()
            movie = Movie.save_movie_in_db(id = id)  

        return movie


class TMDBQueryModel(models.Model):
    page = models.IntegerField()
    timestamp = models.DateTimeField(default = timezone.now)
    total_pages = models.IntegerField(blank = True, null = True)
    total_results = models.IntegerField(blank = True, null = True)
    movies = models.ManyToManyField(Movie, related_name = "%(app_label)s_%(class)s_query+")

    class Meta:
        unique_together = ("page", )
        abstract = True

    # class attributes (to override in children classes)
    update_level = QUERY_UPDATE_LEVEL

    def __str__(self):
        return "page: {0} ({1})".format(self.page, self.timestamp)

    @classmethod
    def get(cls, page, force_update = False):
        try:
            if force_update:
                raise cls.DoesNotExist()

            npq = cls.objects.get(page = page)
            # Update cls when at least one movie is below
            # required update level (it should not happen in practice)
            if any(map(
                lambda update_level: update_level < cls.update_level,
                npq.movies.values_list("update_level", flat=True)
            )):
                raise cls.DoesNotExist()
        except cls.DoesNotExist:
            data = tmdb_request(method = "GET", path = cls.url, 
                params = {"page": page})
            
            # Filter already updated movies
            updated_ids = list(Movie.objects.values_list("id", flat=True).filter(
                id__in=[ int(movie["id"]) for movie in data["results"] ]
            ).filter(update_level__gte=cls.update_level))

            npq, created = cls.objects.update_or_create(
                page = page,
                defaults = {
                    "total_pages": data["total_pages"],
                    "total_results": data["total_results"]
                }
            )
            if not created:
                npq.movies.clear()
                        
            movies2create = list()
            for movie in data["results"]:
                if movie["id"] not in updated_ids:
                    movie["update_level"] = cls.update_level
                    movie_db = Movie.create_movie(
                        id = movie["id"],
                        data = movie
                    )
                    movies2create.append(movie_db)
                    
            movies_ids = list()
            if movies2create:
                movies_ids = [ movie.id for movie in movies2create ]
                Movie.objects.filter(id__in=movies_ids).delete()
                Movie.objects.bulk_create(movies2create)
            
            npq.movies.add(*(movies_ids + updated_ids))

        return npq


class MoviePopularQuery(TMDBQueryModel):
    url = "movie/popular"


class NowPlayingQuery(TMDBQueryModel):
    url = "movie/now_playing"


class UpcomingQuery(TMDBQueryModel):
    url = "movie/upcoming"


class TopRatedQuery(TMDBQueryModel):
    url = "movie/top_rated"