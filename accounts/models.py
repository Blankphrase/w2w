from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from tmdb.models import Movie


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_real = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    mean_rating = models.FloatField(default=0)

    def add_pref(self, id, rating = 10, timestamp = None, 
        save = True, update_mean = True
    ):
        new_pref = self.pref.add(id, rating, timestamp)
        if update_mean:
            self.update_mean_rating(False)
        if save:
            self.save()
        return new_pref


    def add_to_watchlist(self, id):
        return self.watchlist.add(id) # None ?


    def remove_from_watchlist(self, id):
        return self.watchlist.remove(id)


    def get_pref(self, id):
        return self.pref.data.get(movie__id=id)


    def remove_pref(self, id):
        return self.pref.remove(id)


    def update_mean_rating(self, save = True):
        ratings = self.pref.data.values("rating").all()
        self.mean_rating = sum(item["rating"] for item in ratings)/len(ratings)      
        if save:
            self.save()


    def update_profile(self, data):
        self.email = data.get("email", self.email)
        self.save()
        self.profile.update(data)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    # Create associated profile
    try:
        UserProfile.objects.get(user=instance)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

    # Create associated preferences list
    try:
        PrefList.objects.get(user=instance)
    except PrefList.DoesNotExist:
        PrefList.objects.create(user=instance)

    # Create associated watchlist
    try:
        WatchList.objects.get(user=instance)
    except WatchList.DoesNotExist:
        WatchList.objects.create(user=instance)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = "profile",
        blank = False,
        null = False
    )

    MALE = "M"
    FEMALE = "F"
    SEX = ((MALE, "Male"),(FEMALE, "Female"))  

    birthday = models.DateTimeField(blank = True, null = True)
    country = models.CharField(blank = True, null = True, max_length = 255)
    sex = models.CharField(blank = True, null = True, max_length = 1, 
        choices=SEX)

    def update(self, data):
        self.country = data.get("country", self.country)
        self.sex = data.get("sex", self.sex)
        self.birthday = data.get("birthday", self.birthday)
        self.save()


class PrefList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = "pref",
        blank = True,
        null = True
    )

    # models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "pref")
    movies = models.ManyToManyField(Movie, through = "MoviePref",
        related_name = "preflist")

    def add(self, id, rating = 10, timestamp = None, save = True):
        movie = Movie.objects.get(id = id)
        timestamp = timestamp if timestamp else timezone.now()

        try: # update preferences 
            pref_movie = MoviePref.objects.get(preflist = self, movie = movie)
            pref_movie.rating = rating
            pref_movie.timestamp = timestamp
        except MoviePref.DoesNotExist: # new preferences
            pref_movie = MoviePref(
                preflist = self,
                movie = movie,
                rating = rating,
                timestamp = timestamp
            )
        if save:
            pref_movie.save()
        return pref_movie


    def remove(self, id):
        try:
            pref_movie = MoviePref.objects.get(preflist = self, movie__id = id)
            pref_movie.delete()
            return 1
        except MoviePref.DoesNotExist:
            return 0

        
class MoviePref(models.Model):
    preflist = models.ForeignKey(PrefList, related_name = "data")
    movie = models.ForeignKey(Movie, related_name = "ratings")
    rating = models.FloatField()
    timestamp = models.DateTimeField(default = timezone.now)


class WatchList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = "watchlist",
        blank = False,
        null = False
    )

    # Do not create related objects in Movie
    movies = models.ManyToManyField(Movie, related_name = "watchlist+")

    def add(self, id):
        movie = Movie.objects.get(id = id)
        self.movies.add(movie)

    def remove(self, id):
        try:
            self.movies.get(id = id).delete()
            return 1
        except Movie.DoesNotExist:
            return 0