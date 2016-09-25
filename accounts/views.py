from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required

from accounts.forms import SignUpForm, LoginForm, INVALID_LOGIN_ERROR


User = get_user_model()


def signup_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()
        
    return render(request, "accounts/signup.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email = email, password = password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error(field = None, error = INVALID_LOGIN_ERROR)
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_user(request):
    logout(request)
    return redirect("/")