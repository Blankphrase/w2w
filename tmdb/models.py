from django.db import models


class Movie(models.Model):
    title = models.TextField()
    tmdb_id = models.IntegerField()

    class Meta:
        unique_together = ("tmdb_id",)

    def __str__(self):
        return self.title


class MoviePopularQuery(models.Model):
    page = models.IntegerField()
    timestamp = models.DateTimeField()
    total_pages = models.IntegerField(blank = True, null = True)
    total_results = models.IntegerField(blank = True, null = True)
    movies = models.ManyToManyField(Movie)

    class Meta:
        unique_together = ("page",)

    def __str__(self):
        return "page: {0}/{1}".format(self.page, self.timestamp)