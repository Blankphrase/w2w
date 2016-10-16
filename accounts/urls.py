from django.conf.urls import url

from accounts import views

app_name = "accounts"
urlpatterns = [
    url(r"^signup$", views.signup_user, name = "signup"),
    url(r"^login$", views.login_user, name = "login"),
    url(r"^logout$", views.logout_user, name = "logout"),
    url(r"^user/prefs/load$", views.load_prefs, name = "load_prefs"),
    url(r"^user/prefs/update$", views.update_prefs, name = "update_prefs"),
    url(r"^user/prefs/remove$", views.remove_prefs, name = "remove_prefs"),
    url(r"^profile$", views.profile, name = "profile"),
    url(r"^prefs$", views.prefs, name = "prefs"),
    url(r"^watchlist$", views.watchlist, name = "watchlist"),
    url(r"^watchlist/add$", views.watchlist_add, name= "watchlist_add"),
    url(r"^watchlist/remove$", views.watchlist_remove, name = "watchlist_remove"),
    url(r"^recos$", views.recos, name = "recos"),
    url(r"^reco/(\d+)/$", views.reco, name = "reco"),
    url(r"^reco/(\d+)/title$", views.reco_title, name = "reco_title"),
    url(r"^password$", views.password, name = "password")
]
