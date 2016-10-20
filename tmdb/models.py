from django.db import models
from django.utils import timezone

from tmdb.util import tmdb_request


MIN_UPDATE_LEVEL = 0
POPULAR_UPDATE_LEVEL = 1
SEARCH_UPDATE_LEVEL = 1
NOWPLAYING_UPDATE_LEVEL = 1
MOVIE_UPDATE_LEVEL = 2
MAX_UPDATE_LEVEL = 2


class Movie(models.Model):
    id = models.IntegerField(primary_key = True)
    update_level = models.IntegerField(default = 0)
    title = models.TextField()
    poster_path = models.TextField(blank = True, null = True)
    overview = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.title


    @staticmethod
    def download_movie(id):
        data = tmdb_request(method = "GET", path = "movie/%s" % (id))
        if data.get("status_code", None) == 34:
            raise Movie.DoesNotExist()
        data["update_level"] = MOVIE_UPDATE_LEVEL        
        return data

    @staticmethod
    def create_movie(id, data = None):
        if data is None:
            data = Movie.download_movie(id)

        fields_to_update = [ field.name for field in Movie._meta.get_fields() ]
        data = { key: value for key, value in data.items() 
            if key in fields_to_update }

        movie = Movie(**data)
        return movie      

    @staticmethod
    def save_movie_in_db(id, data = None):
        if data is None:
            data = Movie.download_movie(id)

        fields_to_update = [ field.name for field in Movie._meta.get_fields() ]
        data = { key: value for key, value in data.items() 
            if key in fields_to_update }

        movie, created = Movie.objects.update_or_create(
            id = id, defaults = data
        )    
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
    movies = models.ManyToManyField(Movie, related_name = "+")

    class Meta:
        unique_together = ("page", )
        abstract = True

    # class attributes (to override in children classes)
    update_level = None
    url = None

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
            updated_movies = Movie.objects.filter(
                id__in=[ int(movie["id"]) for movie in data["results"] ]
            ).filter(update_level__gte=cls.update_level)
            updated_ids = [ movie.id for movie in updated_movies ]

            npq, created = cls.objects.update_or_create(
                page = page,
                defaults = {
                    "total_pages": data["total_pages"],
                    "total_results": data["total_results"]
                }
            )
            if not created:
                npq.movies.clear()
            npq.movies.add(*updated_movies)
                        
            for movie in data["results"]:
                if movie["id"] not in updated_ids:
                    movie["update_level"] = cls.update_level
                    movie_db = Movie.save_movie_in_db(
                        id = movie["id"],
                        data = movie
                    )
                    npq.movies.add(movie_db)
        return npq


class MoviePopularQuery(TMDBQueryModel):
    update_level = 1
    url = "movie/popular"


class NowPlayingQuery(TMDBQueryModel):
    update_level = 1
    url = "movie/now_playing"


class UpcomingQuery(TMDBQueryModel):
    update_level = 1
    url = "movie/upcoming"


class TopRatedQuery(TMDBQueryModel):
    update_level = 1
    url = "movie/top_rated"