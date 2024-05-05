from django import forms
from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'country', 'phone_number', 'address', 'shipping_address', 'town_city', 'zip_code', 'order_notes', 'total_price']