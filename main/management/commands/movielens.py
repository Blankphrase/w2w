from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from tmdb.models import Movie
from accounts.models import MoviePref, PrefList

import csv
import os
import datetime
import pandas as pd


class Command(BaseCommand):
    '''
    Load MovieLens to database. User specifiy path to
    directory with required csv files: links.csv, movies.csv, ratings.csv.
    '''
    help = "Load data from MovieLens"

    def add_arguments(self, parser):
        parser.add_argument('path', nargs=1, type=str)
        parser.add_argument("--batch", type=int, default=1000, required=False)

        parser.add_argument('--movies', dest="movies", action="store_true")
        parser.add_argument('--no-movies', dest="movies", action="store_false")
        parser.set_defaults(movies=True)

        parser.add_argument("--ratings", dest="ratings", action="store_true")
        parser.add_argument('--no-ratings', dest="ratings", action="store_false")
        parser.set_defaults(ratings=True)

        parser.add_argument("--ratings-file", dest="ratings_file", 
            default="ratings.csv")


    def handle(self, *args, **options):
        path = options.get("path")[0]
        batch = options.get("batch")
        load_movies = options.get("movies")
        load_ratings = options.get("ratings")
        ratings_file = options.get("ratings_file")


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

        if load_movies:

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
            self.stdout.write("Creating movies in database ...")
            movies2create = list()
            movies_id = set()
            for movie in movies:
                if movie["id"] in movies_id:
                    continue
                movies_id.add(movie["id"])
                try:    
                    Movie.objects.get(id = movie["id"])
                except Movie.DoesNotExist:
                    movies2create.append(
                        Movie(id = movie["id"], title = movie["title"])
                    )
                if len(movies2create) > batch:
                    print(" - insarting ...")
                    Movie.objects.bulk_create(movies2create)
                    movies2create = list()
            if len(movies2create) > 0:
                Movie.objects.bulk_create(movies2create)


        if load_ratings:

            User = get_user_model()

            chunk_index = 0
            for chunk in pd.read_csv(
                os.path.join(path, ratings_file), 
                chunksize = 100000
            ):
                self.stdout.write("Processing ratings.csv (chunk: %d) ..." % 
                    chunk_index)

                users = dict()

                df = pd.DataFrame(chunk)
                for index, row in df.iterrows():
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

                # Create artificial users and their favourite movies list
                self.stdout.write("Populating database with users ...")
                users2create = list()
                new_users = list()
                for user in users:
                    try:
                        user_db = User.objects.get(
                            email = "user_%s.movielens@umn.edu" % user
                        )
                    except User.DoesNotExist:
                        user_db = User(
                            email = "user_%s.movielens@umn.edu" % user, 
                            is_real = False, 
                            password = "movielens"
                        )
                        new_users.append(user)
                        users2create.append(user_db)

                    if len(users2create) > batch:
                        print(" - insarting ...")
                        User.objects.bulk_create(users2create)
                        users2create = list()
                if len(users2create) > 0:
                    User.objects.bulk_create(users2create)

                print("%d users saved." % len(new_users))

                self.stdout.write("Creating users' preferences lists ...")
                prefs2create = list()
                for user in new_users:
                    user_db = User.objects.get(email="user_%s.movielens@umn.edu" % user)
                    pref_db = PrefList(user = user_db)
                    prefs2create.append(pref_db)
                    if len(prefs2create) > batch:
                        print(" - insarting ...")
                        PrefList.objects.bulk_create(prefs2create)
                        prefs2create = list()
                if len(prefs2create) > 0:
                    PrefList.objects.bulk_create(prefs2create)    

                print("%d preferences lists saved." % PrefList.objects.count())

                self.stdout.write("Populating database with preferences ...")
                prefs2create = list()
                for user in users:
                    user_db = User.objects.get(email="user_%s.movielens@umn.edu" % user)
                    preflist_db = user_db.pref
                    for pref in users[user]:
                        timestamp = datetime.datetime.fromtimestamp(int(pref["timestamp"]))
                        timestamp = timezone.make_aware(timestamp, 
                            timezone.get_current_timezone())
                        movie = Movie.objects.get(id = pref["id"])
                        pref_db = MoviePref(
                            preflist = preflist_db,
                            movie = movie,
                            rating = self.adjust_rating(int(pref["rating"])), 
                            timestamp = timestamp
                        )
                        prefs2create.append(pref_db)
                    if len(prefs2create) > batch:
                        print(" - insarting ...")
                        MoviePref.objects.bulk_create(prefs2create)
                        prefs2create = list()
                if len(prefs2create) > 0:
                    MoviePref.objects.bulk_create(prefs2create)        

                print("%d preferences saved." % MoviePref.objects.count()) 

                chunk_index += 1     


    def adjust_rating(self, rating):
        return rating