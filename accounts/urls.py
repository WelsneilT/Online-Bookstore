from django.urls import path

from .views import SignUpView, CustomLogoutView, PasswordChangeDoneView, ChangePasswordView, AccountView, update_profile, user_orders

from .views import SignUpView, CustomLogoutView, PasswordChangeView, PasswordResetView

from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('my_account/',ChangePasswordView.as_view(), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts_detail/', AccountView.as_view(), name='my-account'),
    
    path('password_change/', PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('profile/update/', update_profile, name='update_profile'),
    path('orders/',user_orders,name = 'user_orders'),
    
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),
     
]