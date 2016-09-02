from django.http.response import HttpResponse, JsonResponse
from django.forms import model_to_dict

from tmdb.client import Client
from tmdb.settings import TMDB_MAX_PAGE, TMDB_MIN_PAGE


def movies_page(request, page):
    page = int(page)
    request.session["browse_page"] = page
    
    if page < TMDB_MIN_PAGE:
        return JsonResponse({"movies": [], "page": TMDB_MIN_PAGE-1, 
            "total_pages": 0, "total_results": 0})
    elif page > TMDB_MAX_PAGE:
        return JsonResponse({"movies": [], "page": TMDB_MAX_PAGE+1,
            "total_pages": 0, "total_results": 0})
    else:
        return _get_popular_movies(page)


def movies_popular(request):
    page = request.POST.get("page", 1)
    request.session["browse_mode"] = "popular"
    return movies_page(request. page)


def movies_search(request):
    page = rquest.POST.get("page", 1)
    query = request.POST.get("query", None)

    request.session["browse_mode"] = "search"
    request.session["browse_page"] = page
    request.session["browse_query"] = query

    return JsonResponse({})


def movies_next(request):
    return movies_page(request, request.session["browse_page"] + 1)


def movies_prev(request):
    return movies_page(request, request.session["browse_page"] - 1)


def _get_popular_movies(page):
    query_result = Client().get_popular_movies(page)
    data = {
        "movies": [ model_to_dict(movie,  fields = [ "title", "tmdb_id" ]) 
            for movie in query_result.movies.all() ],
        "page": page,
        "total_pages": query_result.total_pages,
        "total_results": query_result.total_results
    }
    return JsonResponse(data)
