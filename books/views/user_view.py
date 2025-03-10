from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from books.models.user_model import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.messages import get_messages


# ✅ User Registration View
def user_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        full_name = request.POST["full_name"]
        contact = request.POST["contact"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        profile_picture = request.FILES.get("profile_picture")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create user profile
        user_profile = UserProfile(user=user, full_name=full_name, contact=contact)
        if profile_picture:
            user_profile.profile_picture = profile_picture
        user_profile.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "register.html")

# ✅ User Login View
def user_login(request):
    """Handles user login"""
    storage = get_messages(request)  # ✅ Clears previous messages
    for _ in storage:
        pass  # This marks all messages as read

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")

    return render(request, "login.html")

# ✅ User Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

@login_required
def user_profile(request):
    """View to display user profile details."""
    profile = UserProfile.objects.get(user=request.user)

    return render(request, "profile.html", {"profile": profile})

@login_required
def edit_profile(request):
    """View to allow users to edit their profile details."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        full_name = request.POST["full_name"]
        contact = request.POST["contact"]
        profile_picture = request.FILES.get("profile_picture")

        profile.full_name = full_name
        profile.contact = contact

        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("edit_profile")  # Redirect back to profile page

    return render(request, "edit_profile.html", {"profile": profile})

@login_required
def change_password(request):
    """Allows users to change their password with validation."""
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_new_password = request.POST["confirm_new_password"]

        user = request.user

        # ✅ Validate current password
        if not check_password(current_password, user.password):
            messages.error(request, "Mero Lado.")
            return redirect("change_password")

        # ✅ Validate new password length
        if len(new_password) < 6:
            messages.error(request, "New password must be at least 6 characters long.")
            return redirect("change_password")

        # ✅ Ensure new passwords match
        if new_password != confirm_new_password:
            messages.error(request, "New passwords do not match.")
            return redirect("change_password")

        # ✅ Change password
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Keeps the user logged in

        messages.success(request, "Password updated successfully!")
        return redirect("my_account")

    return render(request, "change_password.html")

@login_required
def my_account(request):
    """Displays My Account page with Profile & Favorite Books tabs."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    favorite_books = FavoriteBook.objects.filter(user=request.user)

    return render(request, "my_account.html", {
        "profile": profile,
        "favorite_books": favorite_books
    })

@login_required
def add_favorite(request, book_id):
    """Adds a book to favorites."""
    book = get_object_or_404(Book, id=book_id)
    FavoriteBook.objects.get_or_create(user=request.user, book=book)
    return redirect("book_detail", book_id=book.id)  # ✅ Pass book_id

@login_required
def remove_favorite(request, book_id):
    """Removes a book from favorites."""
    book = get_object_or_404(Book, id=book_id)
    FavoriteBook.objects.filter(user=request.user, book=book).delete()
    return redirect("book_detail", book_id=book.id)  # ✅ Pass book_id