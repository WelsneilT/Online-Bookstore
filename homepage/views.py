from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.views import BooksListView
from books.models import Book
# Create your views here.
@login_required
def home(request):
    # Lấy danh sách sách từ model Book
    slider_books = Book.objects.filter(book_available=True)[:6]
    # Trả về trang chính và truyền danh sách sách vào template
    return render(request, 'index-2.html', {'slider_books': slider_books})