# Movies selection section provides two procedures for browsing movies. New
# procedures can be added in the futre, and that why it is important to make
# this as general as possible.
#
# Procedures:
# - most popular (show user the most popular movies)
# - search output (show user movies that where found on the base of the query)

from django.http.request import HttpRequest


import json


def get_movies(settings):
    movies = list()

    if settings["mode"] == "popular":
        if settings["page"] > 0:
            pass
            # request = HttpRequest()
            # request.method = "POST"
            # request.POST["page"] = settings["page"]
            # response = json.loads(movie_popular(request).content.decode())
            # movies = response["results"]
    elif settings["mode"] == "search":
        pass

    return movies