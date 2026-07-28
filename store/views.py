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

from .models import User


MENU_ITEMS = [
    {"title": "Espresso", "category": "Hot Coffee", "description": "Strong and bold espresso with a silky finish.", "price": "4.20", "rating": "4.9", "badge": "Best Seller", "favorites": 180},
    {"title": "Cappuccino", "category": "Hot Coffee", "description": "Velvety espresso topped with creamy foam.", "price": "5.10", "rating": "4.8", "badge": "Popular", "favorites": 160},
    {"title": "Americano", "category": "Hot Coffee", "description": "Smooth black coffee with a mellow body.", "price": "4.50", "rating": "4.7", "badge": "New", "favorites": 140},
    {"title": "Vanilla Latte", "category": "Hot Coffee", "description": "Creamy latte finished with sweet vanilla notes.", "price": "5.80", "rating": "4.9", "badge": "Customer Favorite", "favorites": 220},
    {"title": "Mocha", "category": "Hot Coffee", "description": "Rich espresso blended with premium chocolate.", "price": "6.20", "rating": "4.8", "badge": "Chef Pick", "favorites": 170},
    {"title": "Iced Latte", "category": "Cold Drinks", "description": "Refreshing chilled latte served over ice.", "price": "5.40", "rating": "4.9", "badge": "Fresh", "favorites": 210},
    {"title": "Caramel Cold Brew", "category": "Cold Drinks", "description": "Slow-brewed coffee with a buttery caramel twist.", "price": "5.90", "rating": "4.8", "badge": "Best Seller", "favorites": 205},
    {"title": "Matcha Frappe", "category": "Cold Drinks", "description": "Creamy matcha refreshment with a sweet finish.", "price": "6.10", "rating": "4.7", "badge": "Seasonal", "favorites": 195},
    {"title": "Mango Smoothie", "category": "Cold Drinks", "description": "Bright tropical mango blended to perfection.", "price": "5.70", "rating": "4.6", "badge": "Fresh", "favorites": 190},
    {"title": "Mint Lemon Cooler", "category": "Cold Drinks", "description": "Crisp citrus sparkle with a cooling mint finish.", "price": "4.90", "rating": "4.5", "badge": "New", "favorites": 185},
    {"title": "Chicken Croissant", "category": "Snacks", "description": "Golden croissant filled with seasoned chicken.", "price": "7.40", "rating": "4.6", "badge": "Lunch Pick", "favorites": 175},
    {"title": "Cheese Toastie", "category": "Snacks", "description": "Toasted sandwich packed with melted cheese.", "price": "6.80", "rating": "4.7", "badge": "Popular", "favorites": 172},
    {"title": "Avocado Sandwich", "category": "Snacks", "description": "Creamy avocado layered on soft artisan bread.", "price": "7.20", "rating": "4.8", "badge": "Healthy", "favorites": 165},
    {"title": "Garlic Bread", "category": "Snacks", "description": "Crisp baguette with roasted garlic and herbs.", "price": "4.30", "rating": "4.5", "badge": "Quick Bite", "favorites": 158},
    {"title": "Honey Butter Pancake", "category": "Snacks", "description": "Fluffy pancake brushed with sweet honey butter.", "price": "5.20", "rating": "4.6", "badge": "Morning Favorite", "favorites": 155},
    {"title": "Brownie Bites", "category": "Desserts", "description": "Soft fudgy brownies with a rich chocolate center.", "price": "4.80", "rating": "4.9", "badge": "Sweet Treat", "favorites": 152},
    {"title": "Cheesecake Slice", "category": "Desserts", "description": "Creamy cheesecake with a buttery biscuit base.", "price": "5.60", "rating": "4.8", "badge": "Best Seller", "favorites": 151},
    {"title": "Tiramisu Cup", "category": "Desserts", "description": "Layered coffee sponge dessert with cocoa dusting.", "price": "5.30", "rating": "4.7", "badge": "Chef Pick", "favorites": 146},
    {"title": "Cinnamon Roll", "category": "Desserts", "description": "Soft swirls topped with silky glaze.", "price": "4.90", "rating": "4.6", "badge": "Fresh", "favorites": 142},
    {"title": "Chocolate Lava Cake", "category": "Desserts", "description": "Warm cake with a molten chocolate core.", "price": "6.50", "rating": "4.9", "badge": "Customer Favorite", "favorites": 141},
    {"title": "Chai Tea", "category": "Hot Drinks", "description": "A fragrant spiced tea with a soothing finish.", "price": "3.90", "rating": "4.5", "badge": "Cozy", "favorites": 138},
    {"title": "Hot Chocolate", "category": "Hot Drinks", "description": "Decadent cocoa blended with whipped cream.", "price": "4.70", "rating": "4.7", "badge": "Warm", "favorites": 135},
    {"title": "Chicken Puff", "category": "Snacks", "description": "Flaky pastry filled with savory chicken.", "price": "4.60", "rating": "4.4", "badge": "New", "favorites": 132},
    {"title": "Berry Tart", "category": "Desserts", "description": "Buttery tart filled with fresh berries.", "price": "5.10", "rating": "4.5", "badge": "Seasonal", "favorites": 130},
    {"title": "Dulce de Leche Cookie", "category": "Desserts", "description": "Soft cookie kissed with caramel sweetness.", "price": "3.80", "rating": "4.6", "badge": "Snackable", "favorites": 128},
]


def _get_menu_dataset():
    menu_items = []
    for item in MENU_ITEMS:
        menu_item = dict(item)
        menu_item.setdefault("reviews", 120)
        menu_item.setdefault("discount", "No discount")
        menu_items.append(menu_item)
    return menu_items


def _filter_menu_items(request):
    menu_items = _get_menu_dataset()
    query = request.GET.get("q", "").strip().lower()
    category = request.GET.get("category", "").strip()
    sort_by = request.GET.get("sort", "").strip().lower()

    if query:
        query_terms = query.split()
        menu_items = [
            item
            for item in menu_items
            if all(term in " ".join([item["title"], item["description"], item["category"]]).lower() for term in query_terms)
        ]

    if category and category != "All Categories":
        menu_items = [item for item in menu_items if item["category"] == category]

    if sort_by == "price":
        menu_items = sorted(menu_items, key=lambda item: float(item["price"]))
    elif sort_by == "rating":
        menu_items = sorted(menu_items, key=lambda item: float(item["rating"]), reverse=True)
    elif sort_by == "favorites":
        menu_items = sorted(menu_items, key=lambda item: item.get("favorites", 0), reverse=True)

    return menu_items


def home(request):
    return render(request, "store/home.html")


def menu(request):
    menu_items = _filter_menu_items(request)

    if request.GET.get("ajax") == "1":
        items_per_page = 8
        total_pages = max(1, math.ceil(len(menu_items) / items_per_page))

        page = request.GET.get("page", 1)
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = 1

        page = max(1, min(page, total_pages))
        start = (page - 1) * items_per_page
        end = start + items_per_page
        page_items = menu_items[start:end]

        html = render_to_string("store/components/menu_items.html", {"menu_items": page_items})
        pagination_html = render_to_string(
            "store/components/pagination.html",
            {
                "page": page,
                "total_pages": total_pages,
                "page_numbers": range(1, total_pages + 1),
            },
        )
        return JsonResponse(
            {
                "success": True,
                "items_html": html,
                "pagination_html": pagination_html,
                "page": page,
                "total_pages": total_pages,
            }
        )

    items_per_page = 8
    total_pages = max(1, math.ceil(len(menu_items) / items_per_page))

    page = request.GET.get("page", 1)
    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1

    page = max(1, min(page, total_pages))
    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_items = menu_items[start:end]

    return render(
        request,
        "store/menu.html",
        {
            "menu_items": page_items,
            "page": page,
            "total_pages": total_pages,
            "page_numbers": range(1, total_pages + 1),
        },
    )


def search_suggestions(request):
    menu_items = _filter_menu_items(request)
    suggestions = [
        {"title": item["title"], "category": item["category"]}
        for item in menu_items[:6]
    ]
    return JsonResponse({"success": True, "suggestions": suggestions})


def popular(request):
    return render(request, "store/home.html")


def product_details(request):
    return render(request, "store/product-details.html")


def about(request):
    return render(request, "store/about.html")


def contact(request):
    return render(request, "store/contact.html")


def favorites(request):
    return render(request, "store/favorites.html")


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
                auth_login(request, user)
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
                        auth_login(request, user)
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