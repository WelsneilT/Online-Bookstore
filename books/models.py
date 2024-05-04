from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    rating = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=2000, default=None)
    language = models.CharField(max_length=500)
    genres = models.CharField(max_length=2000, default=None)
    bookFormat = models.CharField(max_length=500)
    edition = models.CharField(max_length=500)
    pages = models.FloatField(null=True, blank=True)
    publisher = models.CharField(max_length=500)
    awards = models.CharField(max_length=500)
    likedPercent = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=2083, default=False)
    price = models.FloatField(null=True, blank=True)
    book_available = models.BooleanField(default=False)

    def __str__(self):
	    return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'