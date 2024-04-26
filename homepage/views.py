from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.models import Book
from django.db.models import Q

@login_required
def home(request):
    slider_books = Book.objects.filter(book_available=True)[406:410]
    featured_products = Book.objects.filter(book_available=True)[96:116]
    new_arrivals = Book.objects.filter(book_available=True)[79:99]
    most_view_products = Book.objects.filter(book_available=True)[221:241]
    adventure_books = Book.objects.filter(book_available=True)[295:300]
    special_offers = Book.objects.filter(book_available=True)[500:505]
    adventure_bookss = Book.objects.filter(
        Q(genres__icontains='Adventure') & Q(book_available=True))[510:520]

    context = {
        'slider_books': slider_books, 
        'featured_products': featured_products, 
        'new_arrivals': new_arrivals, 
        'most_view_products': most_view_products,
        'adventure_books': adventure_books,
        'special_offers': special_offers,
        'adventure_bookss': adventure_bookss
    }

    return render(request, 'index-2.html', context)