from django.urls import include, path
from .views import home, shop_list
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('books/', include('books.urls')),
    path('index-2.html', TemplateView.as_view(template_name='index-2.html'), name='index'),
    path('shop-list/', shop_list, name='shop_list'),
]