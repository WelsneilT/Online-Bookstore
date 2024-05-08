from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255, null=True, blank=True)  # Optional field
    town_city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    order_notes = models.TextField(null=True, blank=True)  # Optional field
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    success = models.BooleanField(default=False)
    canceled_reason = models.CharField(max_length=1000)
    

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
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
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

    def __str__(self):
	    return self.title
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Book,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


