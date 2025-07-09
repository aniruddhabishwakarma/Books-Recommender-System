"""
URL configuration for book_recommender project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from books.views.books_view import home,book_detail,search_books
from books.views.user_view import *
from django.conf import settings
from django.conf.urls.static import static
from books.views.admin_view import *


urlpatterns = [
    path('superadmin/', admin.site.urls),

    # ───── Public Site ─────
    path("", home, name="home"),
    path("search/", search_books, name="search_books"),
    path("book/<str:book_id>/add-to-read/", add_to_read, name="add_to_read"),
    path("book/<str:book_id>/remove-to-read/", remove_to_read, name="remove_to_read"),
    path("book/<str:book_id>/", book_detail, name="book_detail"),

    # ───── User Auth ─────
    path("register/", user_register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),

    # ───── User Account ─────
    path("account/", my_account, name="my_account"),
    path("account/edit-profile/", edit_profile, name="edit_profile"),
    path("account/change-password/", change_password, name="change_password"),
    path("account/favorites/add/<str:book_id>/", add_favorite, name="add_favorite"),
    path("account/favorites/remove/<str:book_id>/", remove_favorite, name="remove_favorite"),

    # ───── Admin Panel ─────
    path('admin/login/', admin_login, name='panel_login'),
    path('admin/logout/', admin_logout, name='panel_logout'),
    path('admin/register/', admin_register, name='panel_register'),
    path('admin/', panel_dashboard, name='panel_dashboard'),
    path("admin/profile/", admin_profile, name="panel_admin_profile"),
    path("admin/books/", admin_books, name="panel_books"),
    path("admin/books/add/", admin_book_add, name="panel_book_add"),
    path("admin/books/<str:book_id>/", admin_book_detail, name="panel_book_detail"),
    path("admin/book/search/", book_search, name="panel_book_search"),
    path("admin/interactions/", admin_interactions_view, name="panel_interactions"),
    path("dashboard/users/", admin_users_view, name="panel_users"),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
