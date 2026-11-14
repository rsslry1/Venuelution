from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import AccountProfile

PROVISIONABLE_ROLES = [
    (AccountProfile.Role.RESIDENT, "Resident"),
    (AccountProfile.Role.VENUE_ADMIN, "Venue Admin"),
    (AccountProfile.Role.EQUIPMENT_ADMIN, "Equipment Admin"),
]


class ProvisionUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=PROVISIONABLE_ROLES, initial=AccountProfile.Role.RESIDENT
    )

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.account_profile.role = self.cleaned_data["role"]
            user.account_profile.save(update_fields=["role"])
        return user


class ProvisionUserChangeForm(UserChangeForm):
    role = forms.ChoiceField(choices=PROVISIONABLE_ROLES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.is_superuser:
            self.fields["role"].choices = [
                (AccountProfile.Role.ADMINISTRATOR, "Administrator")
            ]
            self.fields["role"].disabled = True
        elif self.instance:
            self.fields["role"].initial = self.instance.account_profile.role

    def clean(self):
        cleaned_data = super().clean()
        if (
            self.instance
            and not self.instance.is_superuser
            and cleaned_data.get("is_superuser")
        ):
            self.add_error(
                "is_superuser",
                "Administrator accounts can only be created with createsuperuser.",
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit and not user.is_superuser:
            user.account_profile.role = self.cleaned_data["role"]
            user.account_profile.save(update_fields=["role"])
        return user


class VenuelutionUserAdmin(UserAdmin):
    add_form = ProvisionUserCreationForm
    form = ProvisionUserChangeForm
    add_fieldsets = UserAdmin.add_fieldsets + (("Account role", {"fields": ("role",)}),)
    fieldsets = UserAdmin.fieldsets + (("Account role", {"fields": ("role",)}),)


admin.site.unregister(User)
admin.site.register(User, VenuelutionUserAdmin)
admin.site.register(AccountProfile)
