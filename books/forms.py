from django import forms
from .models import Order, OrderItem, Comment

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'country', 'phone_number', 'address', 'shipping_address', 'town_city', 'zip_code', 'order_notes', 'total_price']

class CommentForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    rating = forms.IntegerField()
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'mb-0 form-control', 'placeholder': 'Enter your comment here...', 'required': 'required'}))