from django.db import models
from django.utils import timezone

from tmdb.util import tmdb_request


MIN_UPDATE_LEVEL = 0
POPULAR_UPDATE_LEVEL = 1
SEARCH_UPDATE_LEVEL = 1
MOVIE_UPDATE_LEVEL = 2
MAX_UPDATE_LEVEL = 2


# data = self._download_movie_data(id)
# data["update_level"] = MAX_UPDATE_LEVEL
# fields_to_update = [
#     field.name for field in Movie._meta.get_fields()\
#         if field.name != "id"
# ]
# Movie.objects.filter(id = id).update(**{
#     key: value for key, value in data.items()\
#         if key in fields_to_update
#     })  



class Movie(models.Model):
    id = models.IntegerField(primary_key = True)
    update_level = models.IntegerField(default = 0)
    title = models.TextField()
    poster_path = models.TextField(blank = True, null = True)
    overview = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.title

    @staticmethod
    def save_movie_in_db(id):
        data = tmdb_request(method = "GET", path = "movie/%s" % (id))
        if data.get("status_code", None) == 34:
            raise Movie.DoesNotExist()
        data["update_level"] = MOVIE_UPDATE_LEVEL      
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


class MoviePopularQuery(models.Model):
    page = models.IntegerField()
    timestamp = models.DateTimeField(default = timezone.now)
    total_pages = models.IntegerField(blank = True, null = True)
    total_results = models.IntegerField(blank = True, null = True)
    movies = models.ManyToManyField(Movie, related_name = "+")

    class Meta:
        unique_together = ("page",)

    def __str__(self):
        return "page: {0}/{1}".format(self.page, self.timestamp)


class NowPlayingQuery(models.Model):
    page = models.IntegerField()
    timestamp = models.DateTimeField(default = timezone.now)
    total_pages = models.IntegerField(blank = True, null = True)
    total_results = models.IntegerField(blank = True, null = True)
    movies = models.ManyToManyField(Movie, related_name = "+")

    class Meta:
        unique_together = ("page", )

    def __str__(self):
        return "page: {0} ({1})".format(self.page, self.timestamp)

    @staticmethod
    def get(page):
        try:
            npq = NowPlayingQuery.objects.get(page = page)
        except:
            data = tmdb_request(method = "GET", path = "movie/nowplaying", 
                params = {"page": 1})
            npq = NowPlayingQuery.objects.create(page = page)
        return npq