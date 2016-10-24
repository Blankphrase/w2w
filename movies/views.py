from django.http.response import HttpResponse, JsonResponse
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from tmdb.client import Client
from tmdb.settings import TMDB_MAX_PAGE, TMDB_MIN_PAGE

import re



def nowplaying_movies(request):
    page = int(request.GET.get("page", 1))
    data = Client().get_nowplaying_movies(page = page)
    return JsonResponse(data)

def upcoming_movies(request):
    page = int(request.GET.get("page", 1))
    data = Client().get_upcoming_movies(page = page)
    return JsonResponse(data)

def toprated_movies(request):
    page = int(request.GET.get("page", 1))
    data = Client().get_toprated_movies(page = page)
    return JsonResponse(data)



@csrf_exempt
def movies_page(request, page):
    page = int(page)
    
    if page < TMDB_MIN_PAGE:
        request.session["browse_page"] = TMDB_MIN_PAGE-1
        return JsonResponse({"movies": [], "page": TMDB_MIN_PAGE-1, 
            "total_pages": 1, "total_results": 0})
    elif page > TMDB_MAX_PAGE:
        request.session["browse_page"] = TMDB_MAX_PAGE+1
        return JsonResponse({"movies": [], "page": TMDB_MAX_PAGE+1,
            "total_pages": 1, "total_results": 0})
    
    request.session["browse_page"] = page

    if request.session["browse_mode"] == "popular":
        data = Client().get_popular_movies(page)
    else:
        query = request.session["browse_query"]
        data = Client().search_movies(query, page)

    return JsonResponse(data)

@csrf_exempt
def movies_popular(request):
    page = request.POST.get("page", 1)
    request.session["browse_mode"] = "popular"
    return movies_page(request, page)

@csrf_exempt
def movies_search(request):
    page = request.POST.get("page", 1)
    query = request.POST.get("query", None)
    if query:
        query = "+".join(re.findall(r"(\w+)", query))   
        
    request.session["browse_mode"] = "search"
    request.session["browse_page"] = page
    request.session["browse_query"] = query

    data = Client().search_movies(query, page)
    return JsonResponse(data)

@csrf_exempt
def movies_next(request):
    return movies_page(request, request.session["browse_page"] + 1)

@csrf_exempt
def movies_prev(request):
    return movies_page(request, request.session["browse_page"] - 1)

@csrf_exempt
def movies_info(request):
    return JsonResponse({
        "mode": request.session["browse_mode"],
        "page": request.session["browse_page"],
        "query": request.session.get("browse_query", None)
    })

def _get_popular_movies(page):
    data = Client().get_popular_movies(page)
    return JsonResponse(data)
