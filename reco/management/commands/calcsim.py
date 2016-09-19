from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from tmdb.models import Movie
from reco.models import MovieSim
from reco.engine import Item2Item

import importlib

class Command(BaseCommand):
    '''
    Calculate similarity between movies.
    '''

    help = "Calculate similarity between movies."

    def add_arguments(self, parser):
        parser.add_argument('simfunc', nargs=1, type=str)

        parser.add_argument('--update-mean-rating', dest="update_mean", 
            action="store_true")
        parser.set_defaults(update_mean=False)


    def handle(self, *args, **options):

        simfunc_name = options.get("simfunc")[0]
        mod = __import__("reco.sims", fromlist=[simfunc_name])
        simfunc = getattr(mod, simfunc_name)

        self.update_users_mean_ratings(*args, **options)

        movie_a = Movie.objects.all()[1000]
        movie_b = Movie.objects.all()[4000]

        sim = simfunc(movie_a, movie_b)
        print(sim)


    def update_users_mean_ratings(self, *args, **options):
        if options.get("update_mean"):
            print("Updating users mean ratings ...")
            User = get_user_model()

            counter = 0
            users_no = User.objects.count()

            for user in User.objects.all():
                user.update_mean_rating()
                counter += 1
                if counter % 100 == 0:
                    print(" -- updated %d users (%2.1f%%)" % (counter, 
                        100*(counter/users_no)))