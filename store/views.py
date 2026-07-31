import json
import math

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import OperationalError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator

from .models import User, Menu_item, Category, Review, Favorite



from django.db.models import Q, Avg, Count

def _filter_menu_items(request):
    menu_items = (
        Menu_item.objects
        .select_related("category")
        .annotate(
            average_rating=Avg("reviews__rating"),
            total_reviews=Count("reviews"),
        )
    )

    query = request.GET.get("q", "").strip()

    if query:
        menu_items = menu_items.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query)
        )

    category = request.GET.get("category")

    if category:
        menu_items = menu_items.filter(
            category__category_name=category
        )

    sort = request.GET.get("sort")

    if sort == "price":
        menu_items = menu_items.order_by("original_price")

    elif sort == "rating":
        menu_items = menu_items.order_by("-average_rating")


    return menu_items


def home(request):
    return render(request, "store/home.html")


def menu(request):
    menu_items = _filter_menu_items(request)

    paginator = Paginator(menu_items, 8)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all().order_by("category_name")

    context = {
    "menu_items": page_obj.object_list,
    "categories": categories,
    "page": page_obj.number,
    "total_pages": paginator.num_pages,
    "page_numbers": paginator.page_range,
    }

    if request.GET.get("ajax") == "1":
        items_html = render_to_string(
            "store/components/menu_items.html",
            context,
            request=request,
        )

        pagination_html = render_to_string(
            "store/components/pagination.html",
            context,
            request=request,
        )

        return JsonResponse({
            "success": True,
            "items_html": items_html,
            "pagination_html": pagination_html,
            "page": page_obj.number,
            "total_pages": paginator.num_pages,
        })


    return render(request, "store/menu.html", context)


def search_suggestions(request):
    menu_items = _filter_menu_items(request)

    suggestions = [
        {
            "title": item.product_name,
            "category": item.category.category_name,
        }
        for item in menu_items[:6]
    ]

    return JsonResponse({
        "success": True,
        "suggestions": suggestions
    })


def _get_product_reviews(product_id):
    return (
        Review.objects
        .filter(product_id=product_id)
        .select_related("user")
        .order_by("-created_at")
    )


def popular(request):
    return render(request, "store/home.html")


def product_details(request, product_id):

    product = (
    Menu_item.objects
    .select_related("category")
    .annotate(
        average_rating=Avg("reviews__rating"),
        total_reviews=Count("reviews"),
    )
    .get(product_id=product_id)
)

    reviews = _get_product_reviews(product_id)

    context = {
        "product": product,
        "reviews": reviews,
    }

    return render(
        request,
        "store/product-details.html",
        context,
    )


def about(request):
    return render(request, "store/about.html")


def contact(request):
    return render(request, "store/contact.html")


@login_required
def favorites(request):

    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related(
            "product",
            "product__category",
        )
        .prefetch_related("product__reviews")
    )

    return render(
        request,
        "store/favorites.html",
        {
            "favorites": favorites,
        },
    )


def user_login(request):
    error_messages = []
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        user = None
        try:
            if email and password:
                user = authenticate(request, email=email, password=password)
        except OperationalError:
            error_messages.append("Unable to connect to the database. Please check your MySQL configuration.")
            return render(request, "store/login.html", {"error_messages": error_messages})
        if user is not None:
            try:
                auth_login(request, user, backend='store.backends.EmailAuthBackend')
            except Exception:
                error_messages.append("Logged in, but unable to update session fields.")
                return render(request, "store/login.html", {"error_messages": error_messages})
            return redirect("home")
        error_messages.append("Invalid email or password.")

    return render(request, "store/login.html", {"error_messages": error_messages})


def user_signup(request):
    error_messages = []
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not email:
            error_messages.append("Email is required.")
        elif password1 != password2:
            error_messages.append("Passwords do not match.")
        else:
            try:
                if User.objects.filter(email=email).exists():
                    error_messages.append("An account already exists for this email.")
                else:
                    full_name = email.split("@", 1)[0].replace(".", " ").replace("_", " ").title()
                    user = User.objects.create(
                        full_name=full_name,
                        email=email,
                        password=make_password(password1),
                        role='Customer',
                    )
                    try:
                        auth_login(request, user, backend='store.backends.EmailAuthBackend')
                    except Exception:
                        error_messages.append("Account created but unable to complete login.")
                        return render(request, "store/signup.html", {"error_messages": error_messages})
                    return redirect("home")
            except OperationalError:
                error_messages.append("Unable to connect to the database. Please check your MySQL configuration.")

    return render(request, "store/signup.html", {"error_messages": error_messages})


def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        new_password1 = request.POST.get("new_password1", "")
        new_password2 = request.POST.get("new_password2", "")

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None and new_password1 and new_password2 and new_password1 == new_password2:
                user.set_password(new_password1)
                user.save(update_fields=["password"])
                messages.success(request, "Password updated successfully.")
                return redirect("login")
            elif user is None:
                messages.error(request, "No account found with that email.")
            else:
                messages.error(request, "Passwords do not match.")

    return render(request, "store/password_reset.html")


def user_logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


@login_required
def profile(request):
    user = request.user
    # Prefer the user's full name if available, otherwise fall back to email
    try:
        if hasattr(user, "get_full_name"):
            name = user.get_full_name() or getattr(user, "email", "")
        else:
            name = getattr(user, "full_name", getattr(user, "email", ""))
    except Exception:
        name = getattr(user, "email", "")

    profile_data = {
        "name": name,
        "email": getattr(user, "email", ""),
        "phone": request.session.get("profile_phone", "+966 5X XXX XXXX"),
        "address": request.session.get("profile_address", "Dammam, Saudi Arabia"),
    }
    return render(request, "store/profile.html", {"profile": profile_data})


@csrf_exempt
@login_required
def update_profile(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Only POST requests are allowed."}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8")) if request.body else {}
    except json.JSONDecodeError:
        payload = request.POST

    if not payload:
        payload = request.POST

    name = payload.get("name") or payload.get("full_name") or "Ahmed Musa"
    email = payload.get("email") or "ahmed@example.com"
    phone = payload.get("phone") or "+966 5X XXX XXXX"
    address = payload.get("address") or "Dammam, Saudi Arabia"

    request.session["profile_name"] = name
    request.session["profile_email"] = email
    request.session["profile_phone"] = phone
    request.session["profile_address"] = address
    request.session.modified = True

    return JsonResponse({"success": True, "message": "Profile updated successfully.", "profile": {"name": name, "email": email, "phone": phone, "address": address}})