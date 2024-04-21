from django.urls import path
from .views import SignUpView, LogOutView
from django.views.generic import RedirectView

urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name = 'signup'),
    path('accounts/logout/', LogOutView.as_view(), name='logout'),
]