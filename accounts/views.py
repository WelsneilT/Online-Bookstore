from pyexpat.errors import messages
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
from django.views.generic import FormView
from .forms import RegistrationForm, PasswordChangingForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django import forms
from django.contrib.auth import update_session_auth_hash


class SignUpView(FormView):
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        # Lấy dữ liệu từ form
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        # Kiểm tra xem người dùng có tồn tại không
        if not User.objects.filter(username=username).exists():
            # Tạo tài khoản mới
            user = User.objects.create_user(username=username, password=password)
            
            # Đăng nhập người dùng tự động sau khi đăng ký
            user = authenticate(username=username, password=password)
            login(self.request, user)
            
            # Chuyển hướng đến trang thành công
            return redirect(self.success_url)
        
        # Nếu tên người dùng đã tồn tại, hiển thị lỗi
        form.add_error('username', 'Username already exists.')
        return self.form_invalid(form)



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
        return reverse('home')  # Redirect to the home page by default

#CHANGE PASSWORD
class PasswordChangeView(FormView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('login')
    template_name = 'password_change.html'
    
    def password_change(request):
        return render(request, "password_change.html")