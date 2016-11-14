from django.conf import settings

TMDB_KEY = getattr(settings, "TMDB_KEY", "be6ac7a5f2a00ea357e5658b5c8731fc")
TMDB_URL = getattr(settings, "TMDB_URL", "https://api.themoviedb.org/3/")

TMDB_FORCE_UPDATE = False