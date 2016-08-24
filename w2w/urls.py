from django.conf.urls import url, include
from django.contrib import admin

from main.views import home_page, browse_movies

urlpatterns = [
    url(r"^$", home_page, name = "home"),
    url(r"^movies/browse/(?P<direction>next|prev)", browse_movies, 
        name = "movies_browse_dir"),
    url(r"^movies/browse/page/(?P<page>\d+)", browse_movies, 
        name = "movies_browse_page"),
    url(r"^movies/browse", browse_movies, name = "movies_browse"),
    url(r"^tmdb/", include("tmdb.urls")),
    url(r'^admin/', admin.site.urls),
]
