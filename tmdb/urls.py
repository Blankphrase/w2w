from django.conf.urls import url, include

from . import views


app_name = "movies"
urlpatterns = [
    url(r"^popular$", views.popular_movies, name="popular_movies"),
    url(r"^search$", views.search_movies, name="search_movies"),
    url(r"^nowplaying$", views.nowplaying_movies, name="nowplaying_movies"),
    url(r"^upcoming$", views.upcoming_movies, name="upcoming_movies"),
    url(r"^toprated$", views.toprated_movies, name="toprated_movies"),
    url(r"^(\d+)/info$", views.movie_info, name="movie_info"),
]
