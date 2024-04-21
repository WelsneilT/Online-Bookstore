from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

class SignUpView(generic.CreateView):
    form_class    = UserCreationForm #hàm cố định
    success_url   = reverse_lazy('login') #đảm bảo rằng việc chuyển hướng chỉ xảy ra sau khi form đã được xử lý xong
    template_name = 'signup.html'


class LogOutView(RedirectView):
    url = reverse_lazy('list')  # Redirect to 'list' page after logout

    @method_decorator(require_POST)  # Ensure this view only handles POST requests to avoid CSRF vulnerability
    def post(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()  # Resets the entire session
        return HttpResponseRedirect(self.url)

