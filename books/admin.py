from django.contrib import admin
from books.models.books_model import Book
from books.models.user_model import AdminProfile, UserProfile # Import models

admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(AdminProfile)


