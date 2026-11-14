from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import AccountProfile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="Full name",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "id": "signup-name",
                "name": "first_name",
                "placeholder": "Your name",
                "autocomplete": "name",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "signup-email",
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "signup-username",
                "placeholder": "Choose a username",
                "autocomplete": "username",
            }
        )
    )
    password1 = forms.CharField(
        label="Create a password",
        widget=forms.PasswordInput(
            attrs={
                "id": "signup-password",
                "placeholder": "At least 8 characters",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm your password",
        widget=forms.PasswordInput(
            attrs={
                "id": "signup-password-confirm",
                "placeholder": "Enter your password again",
                "autocomplete": "new-password",
            }
        ),
    )
    terms_accepted = forms.BooleanField(
        label="I agree to the Terms and Privacy Policy",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Public registration is intentionally resident-only.
            user.account_profile.role = AccountProfile.Role.RESIDENT
            user.account_profile.save(update_fields=["role"])
        return user


class AccountProvisionForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            (AccountProfile.Role.RESIDENT, "Resident"),
            (AccountProfile.Role.VENUE_ADMIN, "Venue Admin / Cultural Department"),
            (AccountProfile.Role.EQUIPMENT_ADMIN, "Equipment Admin / ICONS Department"),
        ]
    )
    first_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.email = self.cleaned_data["email"]
        user.is_active = True
        if commit:
            user.save()
            user.account_profile.role = self.cleaned_data["role"]
            user.account_profile.save(update_fields=["role"])
        return user
