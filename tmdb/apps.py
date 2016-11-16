from django.apps import AppConfig

from tmdb.models import Genre

class TmdbConfig(AppConfig):
    name = 'tmdb'

    def ready(self):
        print("Updating genres ...")
        try:
            Genre.update_genres()
        except:
            pass