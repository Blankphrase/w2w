from django.test import TestCase
from django.utils.html import escape
from django.contrib.auth import get_user_model

from accounts.forms import (
    EMPTY_EMAIL_ERROR, EMPTY_PASSWORD_ERROR, EMPTY_PASSWORD2_ERROR,
    UNIQUE_EMAIL_ERROR, DIFFERENT_PASSWORDS_ERROR,
    SignUpForm
)

User = get_user_model()


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


    def test_password_error_is_shown_on_signup_page(self):
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