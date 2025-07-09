from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Value, CharField, F
from django.db.models.functions import Coalesce

from books.models.books_model import *           # adjust import path
from books.models.user_model import *
from books.decorators import *
import uuid



def admin_register(request):
    """
    Simple admin register view — mirrors user_register logic
    """
    if request.method == "POST":
        username         = request.POST.get("username", "").strip()
        email            = request.POST.get("email", "").strip()
        password         = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm", "")
        full_name        = request.POST.get("full_name", "").strip()
        contact          = request.POST.get("contact", "").strip()
        avatar           = request.FILES.get("profile_picture")

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("panel_register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("panel_register")

        # Create admin user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,      # ✅ flag for admin access
            is_active=True
        )

        # Create admin profile
        profile = AdminProfile.objects.create(
            user=user,
            full_name=full_name,
            contact=contact,
            profile_picture=avatar if avatar else None  # ✅ no validation needed
        )

        messages.success(request, "Admin account created successfully!")
        return redirect("panel_login")

    return render(request, "admin_panel/register.html")


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("panel_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect("panel_dashboard")

        messages.error(request, "Invalid credentials or no panel access.")

    return render(request, "admin_panel/login.html")


def admin_logout(request):
    logout(request)
    return redirect("panel_login")


@admin_required
def panel_dashboard(request):
    total_books         = Book.objects.count()
    total_users         = User.objects.filter(is_staff=False).count()   # only real users
    total_interactions  = FavoriteBook.objects.count() + ToReadBook.objects.count()
    recent_added = Book.objects.order_by('-id')[:5]
    recent_updated = Book.objects.order_by('-id')[:5]

    context = {
        "total_books":        total_books,
        "total_users":        total_users,
        "total_interactions": total_interactions,
        "recent_added": recent_added,
        "recent_updated": recent_updated,
    }
    return render(request, "admin_panel/dashboard.html", context)


@admin_required
def admin_books(request):
    # --- pagination ---
    page_number = request.GET.get("page", 1)
    books_qs    = Book.objects.order_by("title")           # customise ordering if you want
    paginator   = Paginator(books_qs, 25)                  # 25 rows per page
    page_obj    = paginator.get_page(page_number)

    return render(request, "admin_panel/books.html", {
        "page_obj": page_obj,
        "paginator": paginator,
    })

@admin_required
def admin_book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    updated = False

    # ────────── UPDATE (POST) ──────────
    if request.method == "POST":
        book.title           = request.POST.get("title", "").strip()
        book.authors         = request.POST.get("authors", "").strip()
        book.categories      = request.POST.get("categories", "").strip()
        book.published_date  = request.POST.get("published_date", "").strip()
        book.publisher       = request.POST.get("publisher", "").strip()
        book.description     = request.POST.get("description", "").strip()
        book.price           = request.POST.get("price") or None
        book.currency        = request.POST.get("currency", "").strip()
        book.thumbnail       = request.POST.get("thumbnail", "").strip()
        book.info_link       = request.POST.get("info_link", "").strip()
        book.save()
        updated = True

        messages.success(request, "Book updated successfully ✅")
        return redirect("panel_book_detail", book_id=book.id)

    # ────────── READ (GET) ──────────
    return render(request, "admin_panel/admin_book_detail.html", {
        "book": book,
        "updated": updated
        })


def admin_users_view(request):
    users = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 10)  # 10 users per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_panel/users.html", {
        "page_obj": page_obj
    })

@admin_required
def admin_book_add(request):
    """
    Show empty form ➜ POST creates a new Book ➜ redirect to its edit page.
    """
    if request.method == "POST":
        # Generate a unique book ID (feel free to change this rule)
        book_id = str(uuid.uuid4())

        book = Book.objects.create(
            id=book_id,
            title=request.POST.get("title", "").strip(),
            authors=request.POST.get("authors", "").strip(),
            categories=request.POST.get("categories", "").strip(),
            published_date=request.POST.get("published_date", "").strip(),
            publisher=request.POST.get("publisher", "").strip(),
            description=request.POST.get("description", "").strip(),
            price=request.POST.get("price") or None,
            currency=request.POST.get("currency", "").strip(),
            thumbnail=request.POST.get("thumbnail", "").strip(),
            info_link=request.POST.get("info_link", "").strip(),
        )
        # Jump straight to the edit page after creation
        return redirect("panel_book_detail", book_id=book.id)

    # GET  ➜ empty form
    return render(request, "admin_panel/add_book.html")


@admin_required
def admin_profile(request):
    """
    Show & edit the currently-logged-in admin’s profile.
    • GET  ➜ display profile details in a pre-filled form
    • POST ➜ validate + update user & AdminProfile
    """
    user = request.user
    profile, _ = AdminProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # incoming data
        full_name = request.POST.get("full_name", "").strip()
        contact   = request.POST.get("contact", "").strip()
        avatar    = request.FILES.get("profile_picture")   # optional file

        # ── basic validation
        if not full_name:
            messages.error(request, "Full name cannot be empty.")
            return redirect("panel_admin_profile")

        # ── update auth.User (first / last name split)
        parts = full_name.split()
        user.first_name = parts[0]
        user.last_name  = " ".join(parts[1:]) if len(parts) > 1 else ""
        user.save()

        # ── update AdminProfile
        profile.full_name = full_name
        profile.contact   = contact
        if avatar:
            profile.profile_picture = avatar
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("panel_admin_profile")

    # GET  ➜ render template with context
    context = {
        "admin":   user,          # auth.User instance
        "profile": profile        # related AdminProfile (may be empty)
    }
    return render(request, "admin_panel/profile.html", context)

@admin_required
def book_search(request):
    """
    Admin-only search:
      /admin/books/search/?q=<keyword>&page=<n>
    """
    query = request.GET.get("q", "").strip()
    page  = request.GET.get("page", 1)

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(authors__icontains=query)
        ).order_by("-id")              # newest first – tweak as you like
    else:
        messages.info(request, "Enter a keyword to search books.")

    paginator = Paginator(books, 20)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "page_obj": page_obj,
        "query":    query,
    }
    return render(request, "admin_panel/search_results.html", context)


@admin_required
def admin_interactions_view(request):
    fav_qs = FavoriteBook.objects.select_related("user", "book") \
        .annotate(action_type=Value("Favorite", output_field=CharField()),
                  action_date=F("added_on"))

    read_qs = ToReadBook.objects.select_related("user", "book") \
        .annotate(action_type=Value("To-Read", output_field=CharField()),
                  action_date=F("added_on"))

    interactions = list(fav_qs.values(
        "user__username", "book__title", "action_type", "action_date"
    )) + list(read_qs.values(
        "user__username", "book__title", "action_type", "action_date"
    ))

    # All action_date values are datetimes now
    interactions.sort(key=lambda x: x["action_date"], reverse=True)

    page_obj = Paginator(interactions, 25).get_page(request.GET.get("page"))

    return render(request, "admin_panel/interactions.html", {"page_obj": page_obj})


