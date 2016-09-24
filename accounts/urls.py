from django.conf.urls import url
from django.contrib.auth.views import logout

from accounts import views

app_name = "accounts"
urlpatterns = [
    url(r"^signup$", views.signup, name = "signup")
]
