from django.http import JsonResponse
from decimal import Decimal
from books.models import Book
import json
class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        print(basket)
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket
        
    def add(self, object, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(object.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(object.price), 'qty': qty}

        self.save()
    
    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        objects = Book.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in objects:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())
    
    def save(self):
        self.session['skey'] = self.basket
        self.session.modified = True

    def get_total_price(self):
        """Calculate the total price of all items in the basket."""
        return sum(Decimal(item['price']) * item['qty'] for item in self.__iter__())
        
    