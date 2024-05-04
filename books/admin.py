from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Book, Order

# Register Book model with default admin interface
admin.site.register(Book)

# Define the custom admin class for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'created_at', 'order_details']
    search_fields = ['user__username', 'id']
    list_filter = ['created_at', 'updated_at']

    def order_details(self, obj):
        url = reverse('admin_order_detail', args=[obj.id])
        return format_html('<a href="{}">View Details</a>', url)
    order_details.short_description = 'Order Details'

# Register the Order model with the custom admin class
admin.site.register(Order, OrderAdmin)
