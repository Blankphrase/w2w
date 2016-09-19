import math


def cos_sim(movie_a, movie_b):
    rating_a = list(movie_a.preflist.values("user__email", 
        "data__rating").all())
    rating_a = { movie["user__email"]:\
        movie["data__rating"] for movie in rating_a }
    rating_b = list(movie_b.preflist.values("user__email", 
        "data__rating").all())
    rating_b = { movie["user__email"]:\
        movie["data__rating"] for movie in rating_b }

    return _cos_sim(rating_a, rating_b)


def cos_sim_adjusted(movie_a, movie_b):
    rating_a = list(movie_a.preflist.values("user__email", 
        "user__mean_rating", "data__rating").all())
    rating_a = { movie["user__email"]:\
        movie["data__rating"] - movie["user__mean_rating"] for movie in rating_a }
    rating_b = list(movie_b.preflist.values("user__email", 
        "user__mean_rating", "data__rating").all())
    rating_b = { movie["user__email"]:\
        movie["data__rating"] - movie["user__mean_rating"] for movie in rating_b }

    return _cos_sim(rating_a, rating_b)


def _cos_sim(rating_a, rating_b):
    users = [ user for user in rating_a if user in rating_b ]

    len_a, len_b, a_dot_b = 0, 0, 0
    for user in users:
        a_dot_b += rating_a[user]*rating_b[user]
        len_a += rating_a[user]*rating_a[user]
        len_b += rating_b[user]*rating_b[user]

    return a_dot_b/(math.sqrt(len_a*len_b))


# movie_a = Movie.objects.all()[1000]
# movie_b = Movie.objects.all()[2345]

# rating_a = list(movie_a.preflist.values("user__email", 
#     "data__rating").all())
# rating_a = { movie["user__email"]:\
#     movie["data__rating"] for movie in rating_a }
# rating_b = list(movie_b.preflist.values("user__email", 
#     "data__rating").all())
# rating_b = { movie["user__email"]:\
#     movie["data__rating"] for movie in rating_b }


# users = [ user for user in rating_a if user in rating_b ]

# len_a, len_b, a_dot_b = 0, 0, 0
# for user in users:
#     a_dot_b += rating_a[user]*rating_b[user]
#     len_a += rating_a[user]*rating_a[user]
#     len_b += rating_b[user]*rating_b[user]  

# a_dot_b/(math.sqrt(len_a*len_b))
