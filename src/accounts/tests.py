from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationPageTests(TestCase):
    def test_login_page_renders_template_and_signup_fields(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/accounts/login/"')
        self.assertContains(response, 'action="/accounts/signup/"')
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_signup_creates_user_and_signs_them_in(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "first_name": "Alex Resident",
                "username": "alex",
                "email": "alex@example.com",
                "password1": "Strong-local-password-682!",
                "password2": "Strong-local-password-682!",
                "terms_accepted": "on",
            },
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))
        user = User.objects.get(username="alex")
        self.assertEqual(user.first_name, "Alex Resident")
        self.assertTrue(user.check_password("Strong-local-password-682!"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_signup_validation_errors_keep_signup_panel_visible(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "first_name": "Alex",
                "username": "alex",
                "email": "alex@example.com",
                "password1": "Strong-local-password-682!",
                "password2": "a-different-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "is-signup")
        self.assertTrue(response.context["signup_form"].errors)
        self.assertFalse(User.objects.filter(username="alex").exists())

    def test_login_authenticates_user(self):
        User.objects.create_user(username="alex", password="Strong-local-password-682!")

        response = self.client.post(
            reverse("accounts:login"),
            {"username": "alex", "password": "Strong-local-password-682!"},
        )

        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertIn("_auth_user_id", self.client.session)
