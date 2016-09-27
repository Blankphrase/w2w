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
]
