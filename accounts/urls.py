from django.urls import path
from .views import SignUpView, CustomLogoutView
from django.views.generic import RedirectView
from django.contrib.auth.views import PasswordChangeView
from accounts import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('password_change_done/', views.password_change_done, name='password_change_done'),
]