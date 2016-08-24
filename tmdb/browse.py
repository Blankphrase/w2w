# Movies selection section provides two procedures for browsing movies. New
# procedures can be added in the futre, and that why it is important to make
# this as general as possible.
#
# Procedures:
# - most popular (show user the most popular movies)
# - search output (show user movies that where found on the base of the query)

from django.http.request import HttpRequest

from tmdb.views import movie_popular

from abc import ABC, abstractmethod
import json



def get_movies(settings):
    movies = list()

    if settings["mode"] == "popular":
        request = HttpRequest()
        request.method = "POST"
        request.POST["page"] = settings["page"]
        response = json.loads(movie_popular(request).content.decode())
        movies = response["results"]
    elif settings["mode"] == "search":
        pass

    return movies


class BrowseMode(ABC):
    '''
    BrowseMode provides interface for browsing movies in movies selection
    section of the homepage.
    '''

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def prev(self):
        pass

    @abstractmethod
    def has_prev(self):
        pass


class PopularBrowseMode(BrowseMode):
    
    def __init__(self, start_page = 1):
        super(PopularBrowseMode, self).__init__()
        self.cursor = start_page
        self.items = None
        self.pages = None

    def has_next(self):
        if self.pages is None:
            self.load_items(self.cursor)
        return self.cursor <= self.pages

    def next(self):
        self.load_items(self.cursor)
        self.cursor = self.cursor + 1
        return self.items

    def has_prev(self):
        return self.cursor > 1

    def prev(self):
        self.cursor = self.cursor - 1
        self.load_items(self.cursor)
        return self.items

    def load_items(self, page):
        request = HttpRequest()
        request.method = "POST"
        request.POST["page"] = page
        response = json.loads(movie_popular(request).content.decode())
        self.pages = response["total_pages"]
        self.items = response["results"]

    @property
    def total_pages(self):
        if self.pages is None:
            self.load_items(self.cursor)
        return self.pages
    


class SearchBrowseMode(BrowseMode):
    
    def __init__(self, query, items_per_page = 20):
        super(SearchBrowseMode, self).__init__(items_per_page)
        self.query = query