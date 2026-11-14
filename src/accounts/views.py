from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from bookings.models import Booking
from equipment.models import Equipment
from venues.models import Venue

from .forms import AccountProvisionForm, SignUpForm
from .models import AccountProfile


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
        session_age = 14 * 24 * 60 * 60 if self.request.POST.get("remember") else 0
        self.request.session.set_expiry(session_age)
        return response


def signup_view(request):
    form = SignUpForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        user.is_active = False
        user.save(update_fields=["is_active"])
        messages.success(
            request,
            "Your account was created and is waiting for Administrator activation.",
        )
        return redirect("accounts:login")

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
    return render(request, "accounts/dashboard.html", dashboard_context(request.user))


@login_required
def manage_accounts(request):
    if not request.user.is_superuser:
        return redirect("accounts:dashboard")

    form = AccountProvisionForm(request.POST or None)
    if (
        request.method == "POST"
        and request.POST.get("action") == "create"
        and form.is_valid()
    ):
        form.save()
        messages.success(request, "Account created and activated.")
        return redirect("accounts:manage_accounts")

    users = User.objects.select_related("account_profile").order_by("-date_joined")
    return render(
        request,
        "accounts/manage_accounts.html",
        {"form": form, "users": users, "roles": AccountProfile.Role},
    )


@login_required
def update_account(request, pk):
    if not request.user.is_superuser or request.method != "POST":
        return redirect("accounts:dashboard")

    user = User.objects.select_related("account_profile").get(pk=pk)
    action = request.POST.get("action")

    if user == request.user:
        messages.error(
            request, "You cannot change your own Administrator account here."
        )
    elif action == "activate":
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, f"{user.username} is now active.")
    elif action == "deactivate":
        user.is_active = False
        user.save(update_fields=["is_active"])
        messages.success(request, f"{user.username} is now inactive.")
    elif action == "role" and not user.is_superuser:
        allowed_roles = {
            AccountProfile.Role.RESIDENT,
            AccountProfile.Role.VENUE_ADMIN,
            AccountProfile.Role.EQUIPMENT_ADMIN,
        }
        role = request.POST.get("role")
        if role in allowed_roles:
            user.account_profile.role = role
            user.account_profile.save(update_fields=["role"])
            messages.success(request, f"{user.username}'s role was updated.")

    return redirect("accounts:manage_accounts")


def dashboard_context(user):
    role = {
        AccountProfile.Role.ADMINISTRATOR: "admin",
        AccountProfile.Role.VENUE_ADMIN: "venue",
        AccountProfile.Role.EQUIPMENT_ADMIN: "equipment",
    }.get(user.account_profile.role, "resident")

    if role == "resident":
        return resident_dashboard_context(user)

    role_context = {
        "admin": {
            "role_name": "Administrator",
            "dashboard_title": "Administrator overview",
            "primary_nav": "Booking requests",
            "secondary_nav": "Venue & equipment",
            "subheading": "Here is the operational picture across your spaces today.",
            "action_label": "Review requests",
            "queue_title": "Requests needing review",
            "activity_title": "Booking activity",
        },
        "venue": {
            "role_name": "Venue Admin",
            "dashboard_title": "Venue administration",
            "primary_nav": "Booking requests",
            "secondary_nav": "Venues",
            "subheading": "A clear view of venue requests and today's scheduled events.",
            "action_label": "Review requests",
            "queue_title": "Venue requests to review",
            "activity_title": "Venue occupancy",
        },
        "equipment": {
            "role_name": "Equipment Admin",
            "dashboard_title": "Equipment administration",
            "primary_nav": "Equipment requests",
            "secondary_nav": "Inventory",
            "subheading": "Focus on what needs to be prepared, allocated, and returned.",
            "action_label": "Prepare equipment",
            "queue_title": "Equipment to prepare",
            "activity_title": "Equipment allocation",
        },
    }
    context = {"greeting": "Good morning", "role_key": role}
    context.update(role_context[role])
    return dashboard_live_data(user, role, context)


def resident_dashboard_context(user):
    context = {
        "role_key": "resident",
        "role_name": "Resident",
        "dashboard_title": "Resident overview",
        "greeting": "Good morning",
        "primary_nav": "My bookings",
        "secondary_nav": "Available venues",
        "subheading": "Manage your requests and see what is happening at our community spaces.",
        "action_label": "New booking",
        "queue_title": "Your upcoming bookings",
        "activity_title": "Venue availability",
    }
    return dashboard_live_data(user, "resident", context)


def dashboard_live_data(user, role, context):
    today = timezone.localdate()
    now = timezone.now()
    inactive_statuses = [Booking.Status.VENUE_REJECTED, Booking.Status.CANCELLED]
    active_statuses = [
        status
        for status, _ in Booking.Status.choices
        if status not in inactive_statuses
    ]
    bookings = Booking.objects.select_related("resident", "venue")
    role_bookings = bookings.filter(resident=user) if role == "resident" else bookings

    today_bookings = role_bookings.filter(start_at__date=today).exclude(
        status__in=inactive_statuses
    )
    upcoming_bookings = role_bookings.filter(start_at__gte=now).exclude(
        status__in=inactive_statuses
    )
    inventory = Equipment.objects.filter(is_active=True)
    inventory_totals = inventory.aggregate(
        total=Sum("total_quantity"),
        reserved=Sum("reserved_quantity"),
        in_use=Sum("in_use_quantity"),
    )
    available_equipment = sum(item.available_quantity for item in inventory)

    queue = set_dashboard_metrics(
        context,
        role,
        bookings,
        role_bookings,
        today_bookings,
        upcoming_bookings,
        inventory_totals,
        available_equipment,
    )
    set_dashboard_requests(context, queue)
    set_dashboard_schedule(context, today_bookings)
    set_dashboard_chart(context, role_bookings, today, inactive_statuses)

    upcoming_count = upcoming_bookings.count()
    context.update(
        {
            "insight": f"{upcoming_count} active booking{'s' if upcoming_count != 1 else ''} are scheduled from today onward.",
            "today_day": today.day,
            "today_weekday": today.strftime("%A"),
            "today_month_year": today.strftime("%B %Y"),
            "today_label": today.strftime("%A, %d %B"),
        }
    )
    return context


def set_dashboard_metrics(
    context,
    role,
    bookings,
    role_bookings,
    today_bookings,
    upcoming_bookings,
    inventory_totals,
    available_equipment,
):
    pending_count = bookings.filter(status=Booking.Status.PENDING).count()
    reserved_count = inventory_totals["reserved"] or 0
    in_use_count = inventory_totals["in_use"] or 0

    if role == "admin":
        context["metrics"] = [
            {
                "label": "Pending requests",
                "value": pending_count,
                "detail": "Awaiting venue review",
                "trend": f"{today_bookings.count()} today",
            },
            {
                "label": "Active bookings",
                "value": bookings.exclude(
                    status__in=[Booking.Status.VENUE_REJECTED, Booking.Status.CANCELLED]
                ).count(),
                "detail": "Not rejected or cancelled",
                "trend": f"{upcoming_bookings.count()} upcoming",
            },
            {
                "label": "Equipment in use",
                "value": in_use_count,
                "detail": f"{available_equipment} items available",
                "trend": f"{reserved_count} reserved",
            },
        ]
        return bookings.filter(
            status__in=[Booking.Status.PENDING, Booking.Status.CANCELLATION_REQUESTED]
        )

    if role == "venue":
        context["metrics"] = [
            {
                "label": "For approval",
                "value": pending_count,
                "detail": "Venue requests",
                "trend": f"{today_bookings.count()} today",
            },
            {
                "label": "Today's events",
                "value": today_bookings.count(),
                "detail": "Scheduled at active venues",
                "trend": f"{upcoming_bookings.count()} upcoming",
            },
            {
                "label": "Active venues",
                "value": Venue.objects.filter(is_active=True).count(),
                "detail": "Available for booking",
                "trend": "Live",
            },
        ]
        return bookings.filter(status=Booking.Status.PENDING)

    if role == "equipment":
        context["metrics"] = [
            {
                "label": "To prepare",
                "value": bookings.filter(
                    status=Booking.Status.EQUIPMENT_REVIEW
                ).count(),
                "detail": "Equipment requests",
                "trend": f"{today_bookings.count()} today",
            },
            {
                "label": "Reserved items",
                "value": reserved_count,
                "detail": "Allocated to bookings",
                "trend": f"{available_equipment} available",
            },
            {
                "label": "Items in use",
                "value": in_use_count,
                "detail": "Current inventory use",
                "trend": "Live",
            },
        ]
        return bookings.filter(status=Booking.Status.EQUIPMENT_REVIEW)

    context["metrics"] = [
        {
            "label": "Active bookings",
            "value": role_bookings.exclude(
                status__in=[Booking.Status.VENUE_REJECTED, Booking.Status.CANCELLED]
            ).count(),
            "detail": "Your requests and bookings",
            "trend": f"{upcoming_bookings.count()} upcoming",
        },
        {
            "label": "Available venues",
            "value": Venue.objects.filter(is_active=True).count(),
            "detail": "Currently active",
            "trend": "Live",
        },
        {
            "label": "Equipment requests",
            "value": role_bookings.exclude(equipment_requests=None).count(),
            "detail": "Requests with equipment",
            "trend": "Live",
        },
    ]
    return upcoming_bookings


def set_dashboard_requests(context, queue):
    status_classes = {
        Booking.Status.PENDING: "new",
        Booking.Status.VENUE_REJECTED: "urgent",
        Booking.Status.CANCELLATION_REQUESTED: "review",
        Booking.Status.EQUIPMENT_REVIEW: "review",
        Booking.Status.EQUIPMENT_READY: "equipment",
        Booking.Status.CONFIRMED: "new",
        Booking.Status.CANCELLED: "urgent",
    }
    context["requests"] = [
        {
            "day": booking.start_at.strftime("%d"),
            "month": booking.start_at.strftime("%b").upper(),
            "title": booking.event_name,
            "meta": f"{booking.venue.name} · {booking.expected_attendees} guests",
            "status": booking.get_status_display(),
            "status_class": status_classes.get(booking.status, "equipment"),
        }
        for booking in queue.order_by("start_at")[:3]
    ] or [
        {
            "day": "-",
            "month": "",
            "title": "No requests to show",
            "meta": "New requests will appear here.",
            "status": "Clear",
            "status_class": "new",
        }
    ]


def set_dashboard_schedule(context, today_bookings):
    context["schedule"] = [
        {
            "time": booking.start_at.strftime("%H:%M"),
            "title": booking.event_name,
            "place": booking.venue.name,
            "dot": "green" if index == 0 else "gold" if index == 1 else "soft",
        }
        for index, booking in enumerate(today_bookings.order_by("start_at")[:3])
    ] or [{"time": "—", "title": "No events scheduled", "place": "", "dot": "soft"}]


def set_dashboard_chart(context, role_bookings, today, inactive_statuses):
    dates = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
    context["chart"] = [
        role_bookings.filter(start_at__date=day)
        .exclude(status__in=inactive_statuses)
        .count()
        for day in dates
    ]
