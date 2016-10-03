from django.db import models
from django.utils import timezone

MIN_UPDATE_LEVEL = 0
MAX_UPDATE_LEVEL = 2


class Movie(models.Model):
    id = models.IntegerField(primary_key = True)
    update_level = models.IntegerField(default = 0)
    title = models.TextField()
    poster_path = models.TextField(blank = True, null = True)
    overview = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.title


class MoviePopularQuery(models.Model):
    page = models.IntegerField()
    timestamp = models.DateTimeField(default = timezone.now)
    total_pages = models.IntegerField(blank = True, null = True)
    total_results = models.IntegerField(blank = True, null = True)
    movies = models.ManyToManyField(Movie)

    class Meta:
        unique_together = ("page",)

    def __str__(self):
        return "page: {0}/{1}".format(self.page, self.timestamp)

