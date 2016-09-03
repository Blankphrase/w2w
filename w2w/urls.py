from django.conf.urls import url, include
from django.contrib import admin

from main.views import home_page

urlpatterns = [
     # url(r'^admin/', admin.site.urls),
    url(r"^$", home_page, name = "home"),
    url(r"^movies/", include("movies.urls"))
]
