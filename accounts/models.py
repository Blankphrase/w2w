from django.db import models
from django.contrib.auth.base_user import (
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

    def add_pref(self, id, rating = 10, timestamp = None):
        self.pref.add_pref(id, rating, timestamp)

    def get_pref(self, id):
        return self.pref.data.get(movie__id=id)

    def del_pref(self, id):
        self.pref.data.get(movie__id=id).delete()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    PrefList.objects.create(user=instance)


class PrefList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True,
        related_name = "pref"
    )

    # models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "pref")
    movies = models.ManyToManyField(Movie, through = "MoviePref",
        related_name = "preflist")

    def add_pref(self, id, rating = 10, timestamp = None):
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
        pref_movie.save()

        
class MoviePref(models.Model):
    preflist = models.ForeignKey(PrefList, related_name = "data")
    movie = models.ForeignKey(Movie, related_name = "rating")
    rating = models.IntegerField()
    timestamp = models.DateTimeField(default = timezone.now)