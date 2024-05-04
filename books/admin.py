from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Book, Order
from .forms import OrderForm

# Register Book model with default admin interface
admin.site.register(Book)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'country', 'phone_number', 'address', 'town_city', 'zip_code', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'address']
    list_filter = ['country', 'created_at']