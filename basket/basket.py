from django.http import JsonResponse
from decimal import Decimal
from books.models import Book
class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket
        
    def add(self, object, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(object.id)

        if product_id in self.basket:
            if qty != 0:
                self.basket[product_id]['qty'] = qty
            else:
                del self.basket[product_id]
                print(product_id)
                self.save()
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

    def get_item(self, product_id):
        """
        Retrieve a specific Book object from the basket based on the product ID
        """
        str_product_id = str(product_id)
        if str_product_id in self.basket:
            item_data = self.basket[str_product_id]
            product = Book.objects.get(id=product_id)
            item_data['product'] = product
            item_data['price'] = Decimal(item_data['price'])
            item_data['total_price'] = item_data['price'] * item_data['qty']
            return item_data
        else:
            return None
        
