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
    path('accounts/', include("accounts.urls")),  # changes
    path('carousel1/', include('carousel1.urls')),
    path('accounts/', include("django.contrib.auth.urls")),   # working for logins
    path('shop-grid.html', TemplateView.as_view(template_name='html/shop-grid.html'), name='shop-grid'),
    path('shop-list.html', TemplateView.as_view(template_name='html/shop-list.html'), name='shop-list'),
    path('product-details-affiliate.html', TemplateView.as_view(template_name='html/product-details-affiliate.html'), name='product-details'),
    path('blog.html', TemplateView.as_view(template_name='html/blog.html'), name='blog'),
    path('blog-details.html', TemplateView.as_view(template_name='html/blog-details.html'), name='blog-details'),
    path('', include('homepage.urls')),  # Đường dẫn gốc dẫn tới trang chủ
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)