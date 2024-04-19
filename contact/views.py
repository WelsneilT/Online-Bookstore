from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import ContactForm

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            html = render_to_string('contact/index.html', {
                'name': name,
                'email': email,
                'content': content,
                'form': form
            })

            send_mail('The contact form subject', 'This is the message', 'nguyentienkhoi210@gmail.com', ['nguyentienkhoi210@gmail.com'], html_message=html)

    else:
        form = ContactForm()

    return render(request, 'contact/index.html', {
        'form': form
    })