from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Book, Order, OrderItem
from .forms import OrderForm

# Register Book model with default admin interface
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'total_price', 'created_at']
    list_filter = ['created_at', 'updated_at', 'country']
    search_fields = ['first_name', 'last_name', 'email', 'user__username']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'book_available']
    list_filter = ['author', 'book_available']
    search_fields = ['title', 'author', 'description']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
    search_fields = ['product__title', 'order__id']

admin.site.register(Order, OrderAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(OrderItem, OrderItemAdmin)