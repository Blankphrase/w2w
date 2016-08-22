from django.conf.urls import url, include
from django.contrib import admin

from main.views import home_page

urlpatterns = [
    url(r"^$", home_page, name = "home"),
    url(r"^tmdb/", include("tmdb.urls")),
    url(r'^admin/', admin.site.urls)
]
