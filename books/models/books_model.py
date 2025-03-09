from django.db import models


class Book(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=500)
    authors = models.TextField(blank=True, null=True)
    categories = models.CharField(max_length=255, blank=True, null=True)
    published_date = models.CharField(max_length=50, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    info_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

