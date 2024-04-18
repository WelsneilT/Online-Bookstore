from django.shortcuts import render
from .models import Carousel
from django.http import HttpResponse
# Create your views here.
def HomeView (request):
    carousel = Carousel.objects.all()
    context = {
        'carousel': carousel
    }
    return render(request, 'index-2.html', context)