from books.models import Order,OrderItem
from django.contrib.auth.models import User

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)
    return {'orders':orders}

def order_items(request):
    user_orders = user_orders(request)
    for order in user_orders:
        order_items = OrderItem.objects.filter(order_id = order.pk)
    return {'order_items' : order_items}
