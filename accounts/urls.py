from django.conf.urls import url

from accounts import views

app_name = "accounts"
urlpatterns = [
    url(r"^signup$", views.signup_user, name = "signup"),
    url(r"^login$", views.login_user, name = "login"),
    url(r"^logout$", views.logout_user, name = "logout")
]
