from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
