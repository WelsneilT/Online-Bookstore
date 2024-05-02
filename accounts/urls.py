from django.urls import path
<<<<<<< HEAD
from .views import SignUpView, CustomLogoutView, PasswordChangeDoneView, ChangePasswordView, AccountView
=======
from .views import SignUpView, CustomLogoutView, PasswordChangeView
>>>>>>> defa7e2d7027707b307f9018719078d4924c9bcb
from django.views.generic import RedirectView
from accounts import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
<<<<<<< HEAD
    path('change_password/',ChangePasswordView.as_view(), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('', AccountView.as_view(), name='my-account'),
=======
    path('password_change/', PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
>>>>>>> defa7e2d7027707b307f9018719078d4924c9bcb
]