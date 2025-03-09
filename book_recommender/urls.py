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


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("book/<str:book_id>/", book_detail, name="book_detail"),
    path("search/", search_books, name="search_books"),
    path("register/", user_register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("account/", my_account, name="my_account"),  # ✅ New "My Account" page
    path("account/edit-profile/", edit_profile, name="edit_profile"),
    path("account/change-password/", change_password, name="change_password"),
    path("account/favorites/add/<str:book_id>/", add_favorite, name="add_favorite"),
    path("account/favorites/remove/<str:book_id>/", remove_favorite, name="remove_favorite"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
