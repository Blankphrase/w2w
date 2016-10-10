from django.test import TestCase
from django.utils.html import escape
from django.contrib.auth import get_user_model

from accounts.forms import (
    EMPTY_EMAIL_ERROR, EMPTY_PASSWORD_ERROR, EMPTY_PASSWORD2_ERROR,
    UNIQUE_EMAIL_ERROR, DIFFERENT_PASSWORDS_ERROR, INVALID_LOGIN_ERROR,
    SignUpForm, LoginForm
)
from tmdb.models import Movie

import json


User = get_user_model()


class ProfileEditTest(TestCase):

    def setUp(self):
        self.login_user()


    def login_user(self, email = "test@jago.com", password = "test"):
        user = User(email = email)
        user.set_password(password)
        user.save()
        self.client.login(email = email, password = password)    
        return user    


    def test_for_rendering_proper_template(self):
        response = self.client.get("/accounts/profile")
        self.assertTemplateUsed(response, "accounts/profile.html")


    def test_for_returning_error_anonymous_users(self):
        self.client.logout()
        response = self.client.get("/accounts/profile")
        self.assertEqual(response.status_code, 302)


    def test_for_rendering_edit_profile_form(self):
        response = self.client.get("/accounts/profile")
        self.assertIsInstance(response.context["form"], EditProfileForm)


class ProfileWatchlistTest(TestCase):
    pass


class ProfilePrefsTest(TestCase):
    pass


class ProfileRecoTest(TestCase):
    pass


class UserPrefsTest(TestCase):

    def setUp(self):
        for i in range(0, 5):
            Movie.objects.create(id = i, title = "movie_%d" % i)


    def tearDown(self):
        Movie.objects.all().delete()


    def login_user(self, email = "test@jago.com", password = "test"):
        user = User(email = email)
        user.set_password(password)
        user.save()
        self.client.login(email = email, password = password)    
        return user    


    def test_load_prefs_error_for_anonymous_users(self):
        response = self.client.get("/accounts/user/prefs/load")
        self.assertEqual(response.status_code, 302)


    def test_load_prefs_required_user(self):
        self.login_user()
        response = self.client.get("/accounts/user/prefs/load")
        self.assertEqual(response.status_code, 200)


    def test_load_prefs_returns_list_of_preferences(self):
        user = self.login_user()
        user.add_pref(id = 0, rating = 10)
        user.add_pref(id = 1, rating = 5)

        response = self.client.get("/accounts/user/prefs/load")
        data = json.loads(response.content.decode())
        
        self.assertEqual(data["status"].upper(), "OK")
        self.assertIn(data["prefs"][0]["id"], [0, 1])


    def test_update_requires_authenticated_user(self):
        response = self.client.get("/accounts/user/prefs/update")
        self.assertEqual(response.status_code, 302)    
        

    def test_update_add_new_preferences(self):
        user = self.login_user()
        user.add_pref(id = 0, rating = 10)
        user.add_pref(id = 1, rating = 5)

        response = self.client.post(
            "/accounts/user/prefs/update",
            {"id": 2, "rating": 8}
        )

        self.assertEqual(user.pref.data.count(), 3)
        movies = list(user.pref.data.values("movie__id").all())
        movies = [ movie["movie__id"] for movie in movies ]
        self.assertIn(2, movies)


    def test_update_modifies_user_preferences(self):
        user = self.login_user()
        user.add_pref(id = 0, rating = 10)
        user.add_pref(id = 1, rating = 5)

        response = self.client.post(
            "/accounts/user/prefs/update",
            {"id": 1, "rating": 8}
        )

        self.assertEqual(user.pref.data.count(), 2)
        movies = list(user.pref.data.values("movie__id", "rating").all())
        movies = { movie["movie__id"]: movie["rating"] for movie in movies }
        self.assertEqual(movies[1], 8)


    def test_update_invalid_post_returns_error(self):
        user = self.login_user()
        user.add_pref(id = 0, rating = 10)
        user.add_pref(id = 1, rating = 5)

        response = self.client.post(
            "/accounts/user/prefs/update",
            {"id": 1}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(data["status"].upper(), "ERROR")


    def test_remove_requires_authenticated_user(self):
        response = self.client.get("/accounts/user/prefs/remove")
        self.assertEqual(response.status_code, 302)        


    def test_remove_removes_user_preferences(self):
        user = self.login_user()
        user.add_pref(id = 0, rating = 10)
        user.add_pref(id = 1, rating = 5)

        response = self.client.post(
            "/accounts/user/prefs/remove",
            {"id": 1}
        )

        self.assertEqual(user.pref.data.count(), 1)
        movies = list(user.pref.data.values("movie__id").all())
        movies = [ movie["movie__id"] for movie in movies ]
        self.assertNotIn(1, movies)


    def test_remove_invalid_post_returns_error(self):
        user = self.login_user()
        user.add_pref(id = 0, rating = 10)
        user.add_pref(id = 1, rating = 5)

        response = self.client.post(
            "/accounts/user/prefs/remove",
            {"id2": 1}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(data["status"].upper(), "ERROR")


    def test_remove_returns_ok_status_for_not_existing_preferences(self):
        user = self.login_user()
        user.add_pref(id = 0, rating = 10)
        user.add_pref(id = 1, rating = 5)

        response = self.client.post(
            "/accounts/user/prefs/remove",
            {"id": 2}
        )
        data = json.loads(response.content.decode())

        self.assertEqual(user.pref.data.count(), 2)
        self.assertEqual(data["status"].upper(), "OK")



class LogInTest(TestCase):

    def test_login_render_proper_template(self):
        response = self.client.get("/accounts/login")
        self.assertTemplateUsed(response, "accounts/login.html")


    def test_login_passes_form_to_template(self):
        response = self.client.get("/accounts/login")
        self.assertIsInstance(response.context["form"], LoginForm)


    def test_invalid_login_renders_login_template(self):
        response = self.client.post("/accounts/login", data={"email": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")       


    def test_valid_login_redirects_to_home_page(self):
        user = User.objects.create(email = "test@jago.com", password = "test")
        user.set_password("test")
        user.save()
        response = self.client.post("/accounts/login", data={
            "email": "test@jago.com",
            "password": "test"
        })
        self.assertEqual(response.status_code, 302)   


    def test_invalid_error_is_shown_on_signup_page(self):
        response = self.client.post('/accounts/login', data={
            "email": "test@jago.com",
            "password": "test"
        })
        self.assertContains(response, escape(INVALID_LOGIN_ERROR))


    def test_empty_email_error_is_shown_on_login_page(self):
        response = self.client.post("/accounts/login", data={"email": ""})
        self.assertContains(response, escape(EMPTY_EMAIL_ERROR))


    def test_empty_password_error_is_shown_on_login_page(self):
        response = self.client.post('/accounts/login', data={
            "email": "test@jago.com",
            "password": ""
        })
        self.assertContains(response, escape(EMPTY_PASSWORD_ERROR))



class SignUpTest(TestCase):
    

    def test_singup_render_proper_template(self):
        response = self.client.get("/accounts/signup")
        self.assertTemplateUsed(response, "accounts/signup.html")


    def test_signup_passes_form_to_template(self):
        response = self.client.get("/accounts/signup")
        self.assertIsInstance(response.context["form"], SignUpForm)


    def test_for_invalid_signup_renders_signup_template(self):
        response = self.client.post("/accounts/signup", data={"email": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")


    def test_for_valid_singup_redirects_to_home_page(self):
        response = self.client.post("/accounts/signup", data={
            "email": "test@jago.com",
            "password": "test_test",
            "password2": "test_test"
        })
        self.assertEqual(response.status_code, 302)


    def test_valid_signup_automatically_logs_in_user(self):
        response = self.client.post("/accounts/signup", data={
            "email": "test@jago.com",
            "password": "test_test",
            "password2": "test_test"
        })       
        user = User.objects.first()
        self.assertTrue(user.is_authenticated())


    def test_for_valid_singup_saves_user_in_database(self):
        response = self.client.post("/accounts/signup", data={
            "email": "test@jago.com",
            "password": "test_test",
            "password2": "test_test"
        })
        self.assertEqual(User.objects.first().email, "test@jago.com")


    def test_empty_email_error_is_shown_on_signup_page(self):
        response = self.client.post("/accounts/signup", data={"email": ""})
        self.assertContains(response, escape(EMPTY_EMAIL_ERROR))


    def test_occupied_email_error_is_shown_on_signup_page(self):
        User.objects.create(email = "test@jago.com", password="test")
        response = self.client.post("/accounts/signup", 
            data={"email": "test@jago.com"})
        self.assertContains(response, escape(UNIQUE_EMAIL_ERROR))


    def test_empty_password_error_is_shown_on_signup_page(self):
        response = self.client.post('/accounts/signup', data={
            "email": "test@jago.com",
            "password": ""
        })
        self.assertContains(response, escape(EMPTY_PASSWORD_ERROR))


    def test_password2_error_is_shown_on_signup_page(self):
        response = self.client.post('/accounts/signup', data={
            "email": "test@jago.com",
            "password": "test",
            "password2": ""
        })
        self.assertContains(response, escape(EMPTY_PASSWORD2_ERROR))


    def test_different_password_error_is_shown_on_signup_page(self):
        response = self.client.post('/accounts/signup', data={
            "email": "test@jago.com",
            "password": "test",
            "password2": "testowo"
        })
        self.assertContains(response, escape(DIFFERENT_PASSWORDS_ERROR))