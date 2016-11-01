from django.conf.urls import url

from main.views import home_page, reco_page, make_reco, about_page

urlpatterns = [
    url(r"^$", home_page, name = "home"),
    url(r"^about$", about_page, name = "about"),
    url(r"^reco", reco_page, name = "reco"),
    url(r"^make_reco", make_reco, name = "make_reco")
]
