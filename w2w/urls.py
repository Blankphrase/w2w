from django.conf.urls import url, include

urlpatterns = [
    url(r"", include("main.urls")),
    url(r"^movies/", include("tmdb.urls")),
    url(r"^accounts/", include("accounts.urls")),
]
