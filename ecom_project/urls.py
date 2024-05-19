"""
URL configuration for ecom_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # changes
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),  # changes
    path('accounts/', include("django.contrib.auth.urls")),   # working for logins
    path('accounts/', include("accounts.urls")),  # changes
    path('homepage/', include('homepage.urls')),
    path('contact/', include('contact.urls' , namespace = 'contact')),  # changes
    path('index2.html', TemplateView.as_view(template_name='contact/index2.html'), name='contact-index2'),
    path('shop-grid.html', TemplateView.as_view(template_name='html/shop-grid.html'), name='shop-grid'),
    path('shop-list.html', TemplateView.as_view(template_name='html/shop-list.html'), name='shop-list'),
    path('product-details-affiliate.html', TemplateView.as_view(template_name='html/product-details-affiliate.html'), name='product-details'),
    path('product-details-left-thumbnail.html', TemplateView.as_view(template_name='html/product-details-left-thumbnail.html'), name='left-thumbnail'),
    path('cart.html', TemplateView.as_view(template_name='html/cart.html'), name='cart'),
    path('checkout.html', TemplateView.as_view(template_name='html/checkout.html'), name='checkout'),
    path('compare.html', TemplateView.as_view(template_name='html/compare.html'), name='compare'),
    path('login-register.html', TemplateView.as_view(template_name='html/login-register.html'), name='login-register'),
    path('my-account.html', TemplateView.as_view(template_name='html/my-account.html'), name='my-account'),
    path('order-complete.html', TemplateView.as_view(template_name='html/order-complete.html'), name='order-complete'),
    path('faq.html', TemplateView.as_view(template_name='html/faq.html'), name='faq'),
    path('contact-2.html', TemplateView.as_view(template_name='html/contact-2.html'), name='contact-2'),
    path('contact.html', TemplateView.as_view(template_name='html/contact.html'), name='contact'),
    path('blog.html', TemplateView.as_view(template_name='html/blog.html'), name='blog'),
    path('blog-details.html', TemplateView.as_view(template_name='html/blog-details.html'), name='blog-details'),
    path('index-2.html', TemplateView.as_view(template_name='index-2.html'), name='index'),
    path('basket/',include('basket.urls', namespace = 'basket')),
    path('', include('homepage.urls')),  # Đường dẫn gốc dẫn tới trang chủ
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)