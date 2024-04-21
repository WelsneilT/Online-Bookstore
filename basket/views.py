# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from books.models import Book
from .basket import Basket
from basket.forms import  AddToBasketForm
from django.contrib.messages.api import add_message

def basket_summary(request):
    basket = Basket(request)
    basket_json = []

    for item in basket.__iter__():
    # Convert Decimal objects to strings
        item['price'] = str(item['price'])
        item['total_price'] = str(item['total_price'])
    # Extract relevant information from Book objects
        book_info = {
            'title': item['product'].title,
            'author': item['product'].author,
            'description': item['product'].description,
            'price': float(item['product'].price),  # Convert to string if needed
            'image_url': item['product'].image_url,
            'follow_author': item['product'].follow_author,
            'book_available': item['product'].book_available,
            'pk':item['product'].pk,
            # Add other relevant fields as needed
        }
        item['product'] = book_info

        basket_json.append(item)
    return render(request, 'basket/summary.html', {'basket': basket_json})


def basket_add(request):
    basket = Basket(request)
    form = AddToBasketForm(request.POST)
    if form.is_valid():
        product_id = form.cleaned_data['productid']
        product_qty = form.cleaned_data['productqty']
        book_object = get_object_or_404(Book, id=product_id)
        basket.add(object=book_object, qty=product_qty)
        
        basketqty = basket.__len__()
        add_message(request, messages.SUCCESS, 'Product added to basket successfully.')  # Set success message
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        # If the form is not valid, display error messages
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')  # Set error message
    
    # Render the same page with the form and message container
    return render(request, 'detail.html', {'form': form})