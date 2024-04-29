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

class ShopBooksListView(ListView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Thêm queryset từ BooksSliderView
        context['books_list'] = Book.objects.filter(book_available=True)[:20]
        context['featured_products'] = Book.objects.filter(book_available=True)[100:120]
        context['new_arrivals'] = Book.objects.filter(book_available=True)[142:162]
        context['most_view_products'] = Book.objects.filter(book_available=True)[29:39]
        context['adventure_books'] = Book.objects.filter(book_available=True)[29:39]
        context['special_offers'] = Book.objects.filter(book_available=True)[49:58]
        context['adventure_bookss'] = Book.objects.filter(book_available=True, genres__exact='Adventure')[29:39]

        # Thêm queryset từ BooksListView
        context['list_books'] = Book.objects.all()[:100]
        return context
    
    template_name = 'html/shop-list.html'
    
class BooksListView(ListView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Thêm queryset từ BooksSliderView
        context['slider_books'] = Book.objects.filter(book_available=True)[:4]
        context['featured_products'] = Book.objects.filter(book_available=True)[100:120]
        context['new_arrivals'] = Book.objects.filter(book_available=True)[142:162]
        context['most_view_products'] = Book.objects.filter(book_available=True)[29:39]
        context['adventure_books'] = Book.objects.filter(book_available=True)[29:39]
        context['special_offers'] = Book.objects.filter(book_available=True)[49:58]
        context['adventure_bookss'] = Book.objects.filter(book_available=True, genres__exact='Adventure')[29:39]

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

