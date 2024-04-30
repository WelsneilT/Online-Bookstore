# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from books.models import Book
from .basket import Basket
from basket.forms import  AddToBasketForm
from django.contrib.messages.api import add_message
from django.views.generic import ListView, DetailView

def basket_summary(request):
    basket = Basket(request)
    basket_json = []

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
    return render(request, 'basket/summary.html', {'basket': basket})


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
#book_list = {}
#def list_checkout(request):
 #   basket = Basket(request)
  #  if request.method == 'POST':
   #     selected_ids = request.POST.getlist('book')
    #    print(selected_ids)
    # Retrieve the book from the Basket based on the provided ID
    #for id in selected_ids:
     #   print(id)
      #  book = basket.get_item(id)
        # Add the book to the book_list dictionary with the ID as key
       # book_list[id] = {
        #'title': book['product'].title,
        #'price' : str(book['price']),
        #'total_price' : str(book['total_price']),
        #'qty': book['qty'],
    # Extract relevant information from Book objects
         #   'id': book['product'].id,
          #  'title': book['product'].title,
           # 'author': book['product'].author,
            #'description': book['product'].description,
            #'price': float(book['product'].price),  # Convert to string if needed
            #'image_url': book['product'].image_url,
            #'book_available': book['product'].book_available,
            #'pk':book['product'].pk,
            # Add other relevant fields as needed
        #}

    #return redirect(request.META.get('HTTP_REFERER', '/'))

def book_checkout_view_summary(request):
    basket = Basket(request)
    book_list = {}
    if request.method == 'POST':
        selected_ids = request.POST.getlist('book')
        print(selected_ids)
    # Retrieve the book from the Basket based on the provided ID
    for id in selected_ids:
        print(id)
        book = basket.get_item(id)
        # Add the book to the book_list dictionary with the ID as key
        book_list[id] = {
        'title': book['product'].title,
        'price' : str(book['price']),
        'total_price' : str(book['total_price']),
        'qty': book['qty'],
    # Extract relevant information from Book objects
            'id': book['product'].id,
            'title': book['product'].title,
            'author': book['product'].author,
            'description': book['product'].description,
            'price': float(book['product'].price),  # Convert to string if needed
            'image_url': book['product'].image_url,
            'book_available': book['product'].book_available,
            'pk':book['product'].pk,
            # Add other relevant fields as needed
        }
    # Retrieve the accumulated book_list from session
    print(book_list)  # Output for debugging purposes
    template_name = 'basket/checkout_summary.html'
    list_display = book_list
    #book_list.clear()
    context = {'book': list_display}  # Pass book_list to the template context
    return render(request, template_name, context)