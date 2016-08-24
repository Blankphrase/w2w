from django.conf.urls import url, include
from django.contrib import admin

from tmdb.views import movie_popular

app_name = "tmdb"
urlpatterns = [
    url(r"^movie/popular", movie_popular, name = "movie_popular")
]
