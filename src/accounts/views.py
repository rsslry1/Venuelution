from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import SignUpForm


class LoginPageView(LoginView):
    template_name = "accounts/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = context["form"]
        context["signup_form"] = SignUpForm()
        context["active_form"] = "login"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        session_duration = 14 * 24 * 60 * 60 if self.request.POST.get("remember") else 0
        self.request.session.set_expiry(session_duration)
        return response


def signup_view(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("accounts:dashboard")

    return render(
        request,
        "accounts/login.html",
        {
            "login_form": AuthenticationForm(),
            "signup_form": form,
            "active_form": "signup",
        },
    )


@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")
