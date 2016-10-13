from django.shortcuts import render, redirect, reverse
from django.urls import reverse
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger

from accounts.forms import (
    SignUpForm, LoginForm, INVALID_LOGIN_ERROR, EditProfileForm
)


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


@login_required
@csrf_exempt
def load_prefs(request):
    prefs = list(request.user.pref.data.order_by("timestamp").
        values("movie__id", "movie__title", "rating").
        annotate(id=F("movie__id"),title=F("movie__title")).
        values("id", "title", "rating").all())
    return JsonResponse({"status": "OK", "prefs": prefs}, safe=False)


@login_required
@csrf_exempt
def update_prefs(request):
    try:
        movie_id = request.POST["id"]
        movie_rating = request.POST["rating"]
        request.user.add_pref(id = movie_id, rating = movie_rating)
        return JsonResponse({"status": "OK"}, safe=False)
    except KeyError:
        return JsonResponse({"status": "ERROR"}, safe=False)


@login_required
@csrf_exempt
def remove_prefs(request):
    try:
        movie_id = request.POST["id"]
        removed = request.user.remove_pref(movie_id)
        return JsonResponse({"status": "OK", "removed": removed}, safe=False)
    except KeyError:
        return JsonResponse({"status": "ERROR"}, safe=False)
    

@login_required
def profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.user, request.POST)
        if form.is_valid():     
            request.user.update_profile(form.cleaned_data)
            return redirect(reverse("accounts:profile"))
    else:
        form = EditProfileForm(request.user)
    return render(request, "accounts/profile.html", {"form": form})


@login_required
def prefs(request):
    page = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 10)

    prefs_db = list(request.user.pref.data.order_by("timestamp").
        values("movie__id", "movie__title", "rating").
        annotate(id=F("movie__id"),title=F("movie__title")).
        values("id", "title", "rating").all())
    paginator = Paginator(prefs_db, page_size)

    try:
        prefs = paginator.page(page)
    except PageNotAnInteger:
        prefs = paginator.page(1)
    except EmptyPage:
        prefs = paginator.page(paginator.num_pages)

    return render(request, "accounts/prefs.html", { "prefs": prefs})