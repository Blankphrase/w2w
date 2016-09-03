from django.conf.urls import url, include

from . import views


app_name = "movies"
urlpatterns = [
    url(r"^popular$", views.movies_popular, name = "movies_popular"),
    url(r"^next$", views.movies_next, name = "movies_next"),
    url(r"^prev$", views.movies_prev, name = "movies_prev"),
    url(r"^page/(?P<page>-?[\d]+)", views.movies_page, name = "movies_page"),
    url(r"^info$", views.movies_info, name = "movies_info"),
    url(r"^search$", views.movies_search, name = "movies_search")
]
