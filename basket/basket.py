class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        request.session.modified = True
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket
        
    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()
    
    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())