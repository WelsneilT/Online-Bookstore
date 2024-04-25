from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
#from accounts.views import LogOutView

class SignUpView(generic.CreateView):
    form_class    = UserCreationForm #hàm cố định
    success_url   = reverse_lazy('login') #đảm bảo rằng việc chuyển hướng chỉ xảy ra sau khi form đã được xử lý xong
    template_name = 'signup.html'


class CustomLogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        # Perform any additional actions before logout, if needed
        # For example, logging the logout event or updating user status
        
        # Log out the user
        logout(request)
        
        # Redirect to the desired URL after logout
        return HttpResponseRedirect(self.get_redirect_url())

    def get_redirect_url(self, *args, **kwargs):
        # Optionally, you can customize the URL to redirect to after logout
        return reverse('list')  # Redirect to the home page by default
