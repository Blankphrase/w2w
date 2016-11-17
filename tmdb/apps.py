from django.apps import AppConfig

# from tmdb.models import Genre

class TmdbConfig(AppConfig):
    name = 'tmdb'

    # def ready(self):
    #     print("Updating genres ... ", end="")
    #     try:
    #         records = Genre.update_genres()
    #         print("%d updated" % records)
    #     except:
    #         print("ERROR")