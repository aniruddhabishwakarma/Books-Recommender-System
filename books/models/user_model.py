from django.db import models
from django.contrib.auth.models import User
from .books_model import Book

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", default="default.jpg")

    def __str__(self):
        return self.user.username
    

class AdminProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True},  # <-- ensures only staff users
        related_name="admin_profile",
    )
    full_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="admin_profile_pics/", default="admin_profile_pics/default_admin.jpg"
    )

    def __str__(self):
        return self.user.username
    

class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('user', 'book')  # ✅ Prevent duplicate favorites

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    

class ToReadBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')