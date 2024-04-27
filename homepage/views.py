from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.models import Book
from django.db.models import Q

@login_required
def home(request):
    slider_books = Book.objects.filter(book_available=True)[406:412]
    featured_products = Book.objects.filter(book_available=True)[96:116]
    new_arrivals = Book.objects.filter(book_available=True)[79:99]
    most_view_products = Book.objects.filter(book_available=True)[221:241]

    adventure_books = Book.objects.filter(
    Q(genres__icontains='Adventure') & Q(book_available=True))[310:320]
    special_offers = Book.objects.filter(book_available=True)[500:505]
    adventure_bookss = Book.objects.filter(
    Q(genres__icontains='Adventure') & Q(book_available=True))[510:520]
    biography_bookss = Book.objects.filter(
    Q(genres__icontains='Biography') & Q(book_available=True))[10:20]
    drama_bookss = Book.objects.filter(
    Q(genres__icontains='Drama') & Q(book_available=True))[510:520]
    fantasy_bookss = Book.objects.filter(
    Q(genres__icontains='Fantasy') & Q(book_available=True))[510:520]
    fiction_bookss = Book.objects.filter(
    Q(genres__icontains='Fiction') & Q(book_available=True))[510:520]
    history_bookss = Book.objects.filter(
    Q(genres__icontains='History') & Q(book_available=True))[510:520]
    horror_bookss = Book.objects.filter(
    Q(genres__icontains='Horror') & Q(book_available=True))[510:520]
    magic_bookss = Book.objects.filter(
    Q(genres__icontains='Magic') & Q(book_available=True))[10:20]
    non_fiction_bookss = Book.objects.filter(
    Q(genres__icontains='Nonfiction') & Q(book_available=True))[510:520]
    romance_bookss = Book.objects.filter(
    Q(genres__icontains='Romance') & Q(book_available=True))[510:520]
    magic_harry_potter_books = Book.objects.filter(
    Q(genres__icontains='Magic') & Q(title__icontains='Harry Potter') & Q(book_available=True))[0:20]
    special_edition_books = Book.objects.filter(
    Q(edition__icontains='Special Edition') & Q(book_available=True))[0:10]

    context = {
        'slider_books': slider_books, 
        'featured_products': featured_products, 
        'new_arrivals': new_arrivals, 
        'most_view_products': most_view_products,
        'adventure_books': adventure_books,
        'special_offers': special_offers,
        'adventure_bookss': adventure_bookss,
        'biography_books': biography_bookss,
        'drama_bookss' : drama_bookss,
        'fantasy_bookss' : fantasy_bookss ,
        'fiction_bookss' : fiction_bookss,
        'history_bookss' : history_bookss , 
        'horror_bookss' : horror_bookss ,
        'magic_bookss' :    magic_bookss,
        'non_fiction_bookss' : non_fiction_bookss,
        'romance_bookss' :   romance_bookss ,
        'magic_harry_potter_books': magic_harry_potter_books,
        'special_edition_books': special_edition_books}

    return render(request, 'index-2.html', context)