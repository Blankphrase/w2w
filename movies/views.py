from django.http.response import HttpResponse, JsonResponse
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from tmdb.client import Client
from tmdb.settings import TMDB_MAX_PAGE, TMDB_MIN_PAGE


@csrf_exempt
def movies_page(request, page):
    page = int(page)
    
    if page < TMDB_MIN_PAGE:
        request.session["browse_page"] = TMDB_MIN_PAGE 
        return JsonResponse({"movies": [], "page": TMDB_MIN_PAGE-1, 
            "total_pages": 0, "total_results": 0})
    elif page > TMDB_MAX_PAGE:
        request.session["browse_page"] = TMDB_MAX_PAGE
        return JsonResponse({"movies": [], "page": TMDB_MAX_PAGE+1,
            "total_pages": 0, "total_results": 0})
    else:
        request.session["browse_page"] = page
        return _get_popular_movies(page)

@csrf_exempt
def movies_popular(request):
    page = request.POST.get("page", 1)
    request.session["browse_mode"] = "popular"
    return movies_page(request, page)

@csrf_exempt
def movies_search(request):
    page = rquest.POST.get("page", 1)
    query = request.POST.get("query", None)

    request.session["browse_mode"] = "search"
    request.session["browse_page"] = page
    request.session["browse_query"] = query

    return JsonResponse({})

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
    })

def _get_popular_movies(page):
    query_result = Client().get_popular_movies(page)
    data = {
        "movies": [ model_to_dict(movie,  fields = [ "title", "id" ]) 
            for movie in query_result.movies.all() ],
        "page": page,
        "total_pages": query_result.total_pages,
        "total_results": query_result.total_results
    }
    return JsonResponse(data)
