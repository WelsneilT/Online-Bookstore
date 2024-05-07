from django.shortcuts import render 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Book, Order
from django.urls import reverse_lazy
from django.db.models import Q # for search method
from django.http import JsonResponse
import json
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
@login_required
def checkout3(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user  # Set the user
            
            print("Total Price of the Order:", new_order.total_price)  # Print the total price
            
            new_order.save()
            return redirect('basket:basket_ordercomplete2')  # Redirect to a confirmation page, etc. 
        else:
            print("Form errors:", form.errors)
    else:
        form = OrderForm()
    return render(request, 'checkout2.html', {'form': form})



def admin_order_detail_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'admin/order_detail.html', {'order': order})

class ShopBooksListView(ListView):
    model = Book
    template_name = 'html/shop-list.html'
    paginate_by = 24  # Số lượng items trên mỗi trang

    def get_queryset(self):
        return Book.objects.filter(book_available=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Thêm queryset từ BooksListView
        context['list_books'] = Book.objects.all()[:100]
        return context
    
    
class BooksListView(ListView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Thêm queryset từ BooksListView
        context['list_books'] = Book.objects.all()[:100]
        return context
    
    template_name = 'list.html'


class BooksDetailView(DetailView):
    model = Book
    template_name = 'detail.html'
    context_object_name = 'product'


class SearchResultsListView(ListView):
	model = Book
	template_name = 'search_results.html'

	def get_queryset(self): # new
		query = self.request.GET.get('q')
		return Book.objects.filter(
		Q(title__icontains=query) | Q(author__icontains=query)
		)

class BookCheckoutView(DetailView):
    model = Book
    template_name = 'checkout.html'
    login_url     = 'login'
    context_object_name = 'product'


def paymentComplete(request):
	body = json.loads(request.body)
	print('BODY:', body)
	product = Book.objects.get(id=body['productId'])
	Order.objects.create(
		product=product
	)
	return JsonResponse('Payment completed!', safe=False)

class BiographyBooksListView(ListView):
    model = Book
    template_name = 'categories/biography.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='Biography')
    
class DramaBooksListView(ListView):
    model = Book
    template_name = 'categories/drama.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='Drama')
    
class FantasyBooksListView(ListView):
    model = Book
    template_name = 'categories/fantasy.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='Fantasy')

class FictionBooksListView(ListView):
    model = Book
    template_name = 'categories/fiction.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='Fiction')

class HistoryBooksListView(ListView):
    model = Book
    template_name = 'categories/history.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='History')

class HorrorBooksListView(ListView):
    model = Book
    template_name = 'categories/horror.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='Horror')

class MagicBooksListView(ListView):
    model = Book
    template_name = 'categories/magic.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='Magic')

class NonFictionBooksListView(ListView):
    model = Book
    template_name = 'categories/non-fiction.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='Nonfiction')

class RomanceBooksListView(ListView):
    model = Book
    template_name = 'categories/romance.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='Romance')

class AdventureBooksListView(ListView):
    model = Book
    template_name = 'categories/adventure.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        # Lọc sách dựa trên thể loại 'Adventure'
        return Book.objects.filter(genres__icontains='Adventure')