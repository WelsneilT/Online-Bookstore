# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from books.models import Book
from .basket import Basket
from basket.forms import  AddToBasketForm
from django.contrib.messages.api import add_message
from django.views.generic import ListView, DetailView
from django.conf import settings
from decimal import Decimal

def basket_ordercomplete2(request):
    basket = Basket(request)
    basket_json = []
    total_price = 0

    for item in basket.__iter__():
    # Convert Decimal objects to strings
        item['price'] = str(item['price'])
        item['total_price'] = str(item['total_price'])
    # Extract relevant information from Book objects
        book_info = {
            'id': item['product'].id,
            'title': item['product'].title,
            'author': item['product'].author,
            'description': item['product'].description,
            'price': float(item['product'].price),  # Convert to string if needed
            'image_url': item['product'].image_url,
            'book_available': item['product'].book_available,
            'pk':item['product'].pk,
            # Add other relevant fields as needed
        }
        item['product'] = book_info

        basket_json.append(item)
    total_price = sum(Decimal(item['price']) * item['qty'] for item in basket_json)  # Calculate total price
    basket.clear()
    return render(request, 'order-complete2.html', {'basket': basket_json, 'total_price': total_price})

def basket_checkout2(request):
    basket = Basket(request)
    basket_json = []
    total_price = 0

    for item in basket.__iter__():
    # Convert Decimal objects to strings
        item['price'] = str(item['price'])
        item['total_price'] = str(item['total_price'])
    # Extract relevant information from Book objects
        book_info = {
            'id': item['product'].id,
            'title': item['product'].title,
            'author': item['product'].author,
            'description': item['product'].description,
            'price': float(item['product'].price),  # Convert to string if needed
            'image_url': item['product'].image_url,
            'book_available': item['product'].book_available,
            'pk':item['product'].pk,
            # Add other relevant fields as needed
        }
        item['product'] = book_info

        basket_json.append(item)
        
    total_price =  basket.get_total_price()
    #  # Calculate total price
    return render(request, 'checkout2.html', {'basket': basket, 'total_price': total_price})

def basket_summary(request):
    basket = Basket(request)
    basket_json = []
    total_price = 0

    for item in basket.__iter__():
    # Convert Decimal objects to strings
        item['price'] = str(item['price'])
        item['total_price'] = str(item['total_price'])
    # Extract relevant information from Book objects
        book_info = {
            'id': item['product'].id,
            'title': item['product'].title,
            'author': item['product'].author,
            'description': item['product'].description,
            'price': float(item['product'].price),  # Convert to string if needed
            'image_url': item['product'].image_url,
            'book_available': item['product'].book_available,
            'pk':item['product'].pk,
            # Add other relevant fields as needed
        }
        item['product'] = book_info

        basket_json.append(item)
    total_price = basket.get_total_price()  # Calculate total price

    return render(request, 'basket/summary.html', {'basket': basket, 'total_price': total_price})
    


def basket_add(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = AddToBasketForm(request.POST)
    if form.is_valid():
        product_id = form.cleaned_data['productid']
        product_qty = form.cleaned_data['productqty']
        book_object = get_object_or_404(Book, id=product_id)
        basket.add(object=book_object, qty=product_qty)
        
        basketqty = basket.__len__()
        #add_message(request, messages.SUCCESS, 'Product added to basket successfully.')  # Set success message
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        # If the form is not valid, display error messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')  # Set error message
    
    # Render the same page with the form and message container
    #if product_qty == 0:
    #return render(request, 'basket/summary.html', {'form':form})
    #return render(request, 'detail.html', {'form': form})

def book_checkout_view_summary(request, id):
    basket = Basket(request)
    book = 0
    for item in basket:
        if item['product'].id == id:
            book = item
    template_name = 'basket/checkout_summary.html'
    context = {'book': book}
    return render(request, template_name, context)