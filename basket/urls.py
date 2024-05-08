from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('',views.basket_summary, name = 'basket_summary'),
    path('add/', views.basket_add, name='basket_add'),
    path('<int:id>/checkout/',views.book_checkout_view_summary, name = 'basket_checkout'),
    path('checkout2/', views.basket_checkout2, name='basket_checkout2'),
    path('ordercomplete2/', views.basket_ordercomplete2, name='basket_ordercomplete2'),
]