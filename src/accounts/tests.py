from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .admin import ProvisionUserCreationForm
from .models import AccountProfile


class AuthenticationPageTests(TestCase):
    def test_login_page_renders_template_and_signup_fields(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/accounts/login/"')
        self.assertContains(response, 'action="/accounts/signup/"')
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_signup_creates_an_inactive_user_pending_administrator_activation(self):
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

        self.assertRedirects(response, reverse("accounts:login"))
        user = User.objects.get(username="alex")
        self.assertEqual(user.first_name, "Alex Resident")
        self.assertTrue(user.check_password("Strong-local-password-682!"))
        self.assertFalse(user.is_active)
        self.assertNotIn("_auth_user_id", self.client.session)

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

    def test_dashboard_uses_the_default_resident_workspace(self):
        user = User.objects.create_user(
            username="alex", first_name="Alex", password="Strong-local-password-682!"
        )
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resident workspace")
        self.assertContains(response, "Your upcoming bookings")

    def test_public_signup_creates_a_resident_role(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "first_name": "Alex Resident",
                "username": "resident",
                "email": "resident@example.com",
                "password1": "Strong-local-password-682!",
                "password2": "Strong-local-password-682!",
                "terms_accepted": "on",
            },
        )

        self.assertRedirects(response, reverse("accounts:login"))
        self.assertEqual(
            User.objects.get(username="resident").account_profile.role,
            AccountProfile.Role.RESIDENT,
        )

    def test_administration_can_provision_a_venue_admin_but_not_an_administrator_role(
        self,
    ):
        form = ProvisionUserCreationForm(
            data={
                "username": "venue-team",
                "password1": "Strong-local-password-682!",
                "password2": "Strong-local-password-682!",
                "role": AccountProfile.Role.VENUE_ADMIN,
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.account_profile.role, AccountProfile.Role.VENUE_ADMIN)
        self.assertNotIn(
            AccountProfile.Role.ADMINISTRATOR, dict(form.fields["role"].choices)
        )

    def test_administrator_can_open_account_management_and_calendar(self):
        administrator = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="Strong-local-password-682!",
        )
        self.client.force_login(administrator)

        accounts_response = self.client.get(reverse("accounts:manage_accounts"))
        calendar_response = self.client.get(reverse("bookings:calendar"))

        self.assertEqual(accounts_response.status_code, 200)
        self.assertContains(accounts_response, "Account management")
        self.assertEqual(calendar_response.status_code, 200)
        self.assertContains(calendar_response, "Calendar")
