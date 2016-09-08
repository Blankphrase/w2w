from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from tdmb.models import Movie
# from accounts.model import FavMovie

import csv


User = get_user_model()


################################################################################

class Command(BaseCommand):
    '''
    Load MovieLens to database. User specifiy path to
    directory with required csv files: links.csv, movies.csv, ratings.csv.
    '''

    def handle(self, *args, **options):
        self.stdout.write("Command test")

# help = "Load data from MovieLens"

# def handle(self, *args, **options):

# path = args[0]

# # Load data from the files
# links = dict()
# with open("links.csv", newline="") as csvfile:
# reader = csv.DictReader(csvfile)
# for  row in reader:
# movie_id = int(row["movieId"])
# tmdb_id = int(row["tmdbId"])
# links[movie_id] = tmdb_id               

# users = dict()
# with open("ratings.csv", newline="") as csvfile:
# reader = csv.DictReader(csvfile)
# for row in reader:
# movie_id = links[int(row["movieId"])]
# movie = { "id": movie_id, "rating": int(row["rating"]),
# "timestamp": row["timestamp"] }

# user_id = row["userId"]
# if user_id not in users:
# users[user_id] = list()     
# users[user_id].append(movie)

# movies = list()
# with open("movies.csv", newline="") as csvfile:
# reader = csv.DictReader(csvfile)
# for row in reader:
# movie_id = links[int(row["movieId"])]
# title = row["title"]
# movies.append({ "id": movie_id, "title": title })


# # Create coressponding movies in database
# for movie in movies:
# try:    
# Movie.objects.get(id = movie["id"])
# except Movie.DoesNotExist:
# Movie.objects.create(id = movie["id"], title=movie["title"])

# # Create artificial users and their favourite movies list
# for user in users:
# user_db = User.objects.create()
# for pref in user:
# user_db.add_pref(id = pref["id"], rating = pref["rating"],
# timestamp = pref["timestamp"])