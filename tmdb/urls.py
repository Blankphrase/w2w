from django.conf.urls import url, include
from django.contrib import admin

from main.views import home_page


app_name = "tmdb"
urlpatterns = [
    url(r"^popular", home_page, name = "home")
]
