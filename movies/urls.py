from django.conf.urls import url, include

from .views import movies_popular, movies_next, movies_prev, movies_page


app_name = "movies"
urlpatterns = [
    url(r"^popular$", movies_popular, name = "movies_popular"),
    url(r"^next$", movies_next, name = "movies_next"),
    url(r"^prev$", movies_prev, name = "movies_prev"),
    url(r"^page/(?P<page>-?[\d]+)", movies_page, name = "movies_page")
]
