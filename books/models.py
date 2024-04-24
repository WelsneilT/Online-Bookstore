from django.db import models
from django.urls import reverse

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
	product = models.ForeignKey(Book, max_length=500, null=True, blank=True, on_delete = models.SET_NULL)
	created =  models.DateTimeField(auto_now_add=True) 

	def __str__(self):
		return self.product.title