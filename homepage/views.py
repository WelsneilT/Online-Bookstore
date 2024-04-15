from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    images = [
        {'url': 'static/website/images/front-view-young-woman-reading-book.jpg'},
        {'url': 'static/website/images/pexels-josh-hild-4256852.jpg'},
        {'url': 'static/website/images/pexels-lepta-studio-13929613.jpg'},
        {'url': 'static/website/images/pexels-pixabay-207607.jpg'},
        {'url': 'static/website/images/pexels-anne-981110.jpg'},
        
        # Add more image dicts
    ]
    return render(request,'index-2.html', {})