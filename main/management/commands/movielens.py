from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from tmdb.models import Movie

import csv
import os
import datetime


class Command(BaseCommand):
    '''
    Load MovieLens to database. User specifiy path to
    directory with required csv files: links.csv, movies.csv, ratings.csv.
    '''
    help = "Load data from MovieLens"

    def add_arguments(self, parser):
        parser.add_argument('path', nargs=1, type=str)

    def handle(self, *args, **options):
        path = options.get("path")[0]

        # Load data from the files
        self.stdout.write("Processing links.csv ...")
        links = dict()
        with open(os.path.join(path, "links.csv"), newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    movie_id = int(row["movieId"])
                    tmdb_id = int(row["tmdbId"])
                    links[movie_id] = tmdb_id       
                except ValueError:
                    pass

        self.stdout.write("Processing ratings.csv ...")
        users = dict()
        with open(os.path.join(path, "ratings.csv"), newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    movie_id = links[int(row["movieId"])]
                    movie = { "id": movie_id, "rating": float(row["rating"]),
                        "timestamp": row["timestamp"] }

                    user_id = row["userId"]
                    if user_id not in users:
                        users[user_id] = list()     
                    users[user_id].append(movie)
                except KeyError:
                    pass

        self.stdout.write("Processing movies.csv ...")
        movies = list()
        with open(os.path.join(path, "movies.csv"), newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    movie_id = links[int(row["movieId"])]
                    title = row["title"]
                    movies.append({ "id": movie_id, "title": title })
                except KeyError:
                    pass

        # Create coressponding movies in database
        # self.stdout.write("Creating movies in database ...")
        # for movie in movies:
        #     try:    
        #         Movie.objects.get(id = movie["id"])
        #     except Movie.DoesNotExist:
        #         Movie.objects.create(id = movie["id"], title=movie["title"])

        User = get_user_model()

        # Create artificial users and their favourite movies list
        self.stdout.write("Populating database with preferences ...")
        for user in users:
            user_db = User.objects.create(
                email = "user_%s.movielens@umn.edu." % user, 
                is_real = False, 
                password = "movielens"
            )
            for pref in users[user]:
                timestamp = datetime.datetime.fromtimestamp(int(pref["timestamp"]))
                user_db.add_pref(
                    id = int(pref["id"]), 
                    rating = self.adjust_rating(int(pref["rating"])), 
                    timestamp = timestamp
                )

    def adjust_rating(self, rating):
        return 2*rating