from django.urls import path
from .views import SignUpView, CustomLogoutView, PasswordChangeDoneView, ChangePasswordView, AccountView
from django.views.generic import RedirectView
from django.contrib.auth.views import PasswordChangeView
from accounts import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('change_password/',ChangePasswordView.as_view(), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('', AccountView.as_view(), name='my-account'),
]