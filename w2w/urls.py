from django.conf.urls import url, include
from django.contrib import admin

from main.views import home_page, reco_page, make_reco

urlpatterns = [
     # url(r'^admin/', admin.site.urls),
    url(r"^$", home_page, name = "home"),
    url(r"^reco", reco_page, name = "reco"),
    url(r"^make_reco", make_reco, name = "make_reco"),
    url(r"^movies/", include("tmdb.urls")),
    url(r"^accounts/", include("accounts.urls")),
]
