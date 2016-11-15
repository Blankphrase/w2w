from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import update_session_auth_hash
from django.template import Context
from django.template.loader import get_template

import w2w.settings
from accounts.forms import (
    SignUpForm, LoginForm, INVALID_LOGIN_ERROR, EditProfileForm,
    ChangePasswordForm, DeleteAccountForm
)
from tmdb.models import Movie
from reco.models import Reco

User = get_user_model()


def signup_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = w2w.settings.AUTHENTICATION_BACKENDS[0]
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
                user.backend = w2w.settings.AUTHENTICATION_BACKENDS[0]
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
    return render(request, "accounts/profile.html", 
        {"form": form, "form_delete": form}
    )


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


@login_required
def watchlist(request):
    page = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 10)

    watchlist_db = list(request.user.watchlist.movies.order_by("title").
        values("id", "title").all())
    paginator = Paginator(watchlist_db, page_size)

    try:
        watchlist = paginator.page(page)
    except PageNotAnInteger:
        watchlist = paginator.page(1)
    except EmptyPage:
        watchlist = paginator.page(paginator.num_pages)
    
    return render(request, "accounts/watchlist.html", {"watchlist": watchlist})


@login_required
@csrf_exempt
def watchlist_add(request):
    try:
        movie_id = request.POST["id"]
    except KeyError:
        return JsonResponse({"status": "ERROR", "msg": "No movie id."}, 
            safe=False)

    try:
        request.user.add_to_watchlist(id = movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({"status": "ERROR", "msg": "Invalid movie id"}, 
            safe=False)

    return JsonResponse({"status": "OK"}, safe=False)


@login_required
@csrf_exempt
def watchlist_remove(request):
    try:
        movie_id = request.POST["id"]
    except KeyError:
        return JsonResponse({"status": "ERROR", "msg": "No movie id."}, 
            safe=False)
    request.user.watchlist.movies.filter(id=movie_id).delete()
    return JsonResponse({"status": "OK"}, safe=False)


@login_required
def recos(request):
    page = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 10)

    recos_db = request.user.recos.order_by("-timestamp").all()
    paginator = Paginator(recos_db, page_size)

    try:
        recos = paginator.page(page)
    except PageNotAnInteger:
        recos = paginator.page(1)
    except EmptyPage:
        recos = paginator.page(paginator.num_pages)

    return render(request, "accounts/recos.html", {"recos": recos})


@login_required
def reco(request, id):
    try:
        reco = Reco.objects.get(id=id, user=request.user)
    except Reco.DoesNotExist:
        return redirect(reverse("accounts:recos"))
    return render(request, "accounts/reco.html", {"reco": reco})


@login_required
@csrf_exempt
def reco_title(request, id):
    try:
        title = request.POST["title"]
    except:
        return JsonResponse({"status": "ERROR", "msg": "No title"}, safe=False)

    try:
        reco = Reco.objects.get(id=id,user=request.user)
    except:
        return JsonResponse({"status": "ERROR", "msg": "No reco"}, safe=False)

    reco.title = title
    reco.save()
    return JsonResponse({"status": "OK"}, safe=False)


@login_required
def password(request):
    password_changed = False
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["new_password"])
            request.user.save()
            update_session_auth_hash(request, request.user)
            password_changed = True
    else:
        form = ChangePasswordForm(request.user)
    return render(request, "accounts/password.html", 
        {"form": form, "password_changed": password_changed})


@login_required
def delete(request):
    if request.method == "POST":
        form = DeleteAccountForm(request.user, request.POST)
        if form.is_valid():
            request.user.delete()
            return redirect(reverse("home"))
    else:
        form = DeleteAccountForm(request.user)
    return render(request, "accounts/delete.html", {"form": form})