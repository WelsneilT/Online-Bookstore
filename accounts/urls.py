from django.urls import path
from .views import SignUpView, CustomLogoutView
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name = 'signup'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
]