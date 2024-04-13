from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import generic


class SignUpView(generic.CreateView):
    form_class    = UserCreationForm #hàm cố định
    success_url   = reverse_lazy('login') #đảm bảo rằng việc chuyển hướng chỉ xảy ra sau khi form đã được xử lý xong
    template_name = 'signup.html'


