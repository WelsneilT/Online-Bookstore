from books.models import Order
from django.contrib.auth.models import User

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)
    return {'orders':orders}