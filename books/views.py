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
from .models import Order,OrderItem
from .forms import OrderForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, CommentForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from basket.basket import Basket
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
import pickle
import pandas as pd
import numpy as np
from django.utils.decorators import method_decorator
from nltk.stem.porter import PorterStemmer
ps= PorterStemmer()
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os
# Load the model from the .pkl file
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
with open('vector.pkl', 'rb') as file:
    vector = pickle.load(file)
# Function to recommend similar books
conn = sqlite3.connect('db.sqlite3')
query = "SELECT * FROM books_book;"
books = pd.read_sql_query(query, conn)
conn.close()

def update_revenue_chart(request):
    # Kết nối với cơ sở dữ liệu SQLite
    conn = sqlite3.connect('db.sqlite3')

    # Truy vấn dữ liệu từ bảng books_order
    query = "SELECT * FROM books_order"
    orders = pd.read_sql_query(query, conn)

    # Đóng kết nối với cơ sở dữ liệu
    conn.close()

    # Chuyển đổi dữ liệu thành DataFrame của pandas
    orders['created_at'] = pd.to_datetime(orders['created_at'])
    data = {
        'id': orders['id'],
        'user_id': orders['user_id'],
        'first_name': orders['first_name'],
        'last_name': orders['last_name'],
        'email': orders['email'],
        'country': orders['country'],
        'phone_number': orders['phone_number'],
        'address': orders['address'],
        'shipping_address': orders['shipping_address'],
        'town_city': orders['town_city'],
        'zip_code': orders['zip_code'],
        'order_notes': orders['order_notes'],
        'total_price': orders['total_price'],
        'created_at': orders['created_at'],
        'updated_at': orders['updated_at'],
        'success': orders['success'],
        'canceled_reason': orders['canceled_reason']
    }

    df = pd.DataFrame(data)

    # Lấy ngày hiện tại
    today = pd.Timestamp.today()

    # Tạo thêm dữ liệu giả lập cho mỗi ngày từ 1/4 đến ngày hiện tại
    date_range = pd.date_range(start='2024-04-01', end=today)
    num_samples = len(date_range)

    np.random.seed(42)
    random_prices = np.random.uniform(low=2.0, high=100.0, size=num_samples)

    additional_data = {
        'id': np.arange(df['id'].max() + 1, df['id'].max() + 1 + num_samples),
        'user_id': [1] * num_samples,  # Giá trị giả lập cho user_id
        'first_name': ['Tống'] * num_samples,
        'last_name': ['Tân'] * num_samples,
        'email': ['td.tan2711@gmail.com'] * num_samples,
        'country': ['Vietnam'] * num_samples,
        'phone_number': ['0327728199'] * num_samples,
        'address': ['25/89 Thịnh Quang'] * num_samples,
        'shipping_address': ['25/89 Thịnh Quang'] * num_samples,
        'town_city': ['Hà Nội'] * num_samples,
        'zip_code': ['000084'] * num_samples,
        'order_notes': [''] * num_samples,
        'total_price': random_prices,
        'created_at': date_range,
        'updated_at': date_range,
        'success': [True] * num_samples,
        'canceled_reason': [''] * num_samples
    }

    additional_df = pd.DataFrame(additional_data)

    # Kết hợp dữ liệu hiện tại với dữ liệu giả lập
    combined_df = pd.concat([df, additional_df], ignore_index=True)

    # Chuẩn bị dữ liệu cho mô hình
    combined_df['date'] = combined_df['created_at'].dt.date
    daily_revenue = combined_df.groupby('date')['total_price'].sum().reset_index()

    # Chuyển đổi cột 'date' thành kiểu datetime và tạo cột 'days'
    daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
    daily_revenue['days'] = (daily_revenue['date'] - daily_revenue['date'].min()).dt.days

    # Chia dữ liệu thành biến độc lập (X) và biến phụ thuộc (y)
    X = daily_revenue[['days']]
    y = daily_revenue['total_price']

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Huấn luyện mô hình hồi quy tuyến tính
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Dự đoán doanh thu ngày tiếp theo
    def predict_next_day_revenue():
        next_day = [[daily_revenue['days'].max() + 1]]
        predicted_revenue = model.predict(next_day)
        next_day_date = daily_revenue['date'].max() + timedelta(days=1)
        return predicted_revenue[0], next_day_date

    predicted_revenue, next_day_date = predict_next_day_revenue()

    # Đánh giá mô hình và hiển thị biểu đồ
    plt.figure(figsize=(12, 6))
    plt.plot(daily_revenue['date'], daily_revenue['total_price'], marker='o', linestyle='-', color='grey', alpha=0.6, label='Actual Revenue')
    plt.scatter(next_day_date, predicted_revenue, color='red', label='Next Day Prediction', marker='X', s=100)
    plt.xlabel('Date')
    plt.ylabel('Revenue')
    plt.title('Actual vs Predicted Revenue')
    plt.legend()
    plt.grid(True)

    # Định dạng lại trục x để hiển thị ngày tháng
    plt.gcf().autofmt_xdate()

    # Lưu biểu đồ thành file hình ảnh
    if not os.path.exists('static/admin'):
        os.makedirs('static/admin')
    plt.savefig('static/admin/revenue_prediction.png')
    plt.close()

    return redirect('revenue-chart')

def revenue_chart_view(request):
    return render(request, 'admin/revenue_chart.html')

def stem_text(text):
    return ' '.join([ps.stem(word) for word in text.split()])

def semantic_search(query, books, tfidf_matrix, tfidf_vectorizer):
    query = stem_text(query)
    query_vector = tfidf_vectorizer.transform([query])
    
    # Calculate cosine similarity between query vector and document vectors
    similarities = cosine_similarity(query_vector, tfidf_matrix)
    ranked_indices = similarities.argsort()[0][::-1]  # Sort by descending order of similarity
    print(similarities)
    # Return ranked documents based on similarity
    ranked_documents = books.iloc[ranked_indices]['title']
    print(ranked_documents)
    print(ranked_indices[0:101])
    return ranked_indices[0:101]

@login_required
def checkout3(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user  # Set the user
            new_order.success = False
            print("Total Price of the Order:", new_order.total_price)  # Print the total price
            new_order.save()
            order_id = new_order.pk
            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty']) 
            return redirect('basket:basket_ordercomplete2')  # Redirect to a confirmation page, etc.
        
        else:
            print("Form errors:", form.errors)
    else:
        form = OrderForm()
    return render(request, 'checkout2.html', {'form': form})



def admin_order_detail_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'admin/order_detail.html', {'order': order})

# class ShopBooksListView(ListView):
#     model = Book
#     template_name = 'html/shop-list.html'
#     paginate_by = 24  # Số lượng items trên mỗi trang

#     def get_queryset(self):
#         return Book.objects.filter(book_available=True)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # Thêm queryset từ BooksListView
#         context['list_books'] = Book.objects.all()[:100]
#         return context
class ShopBooksListView(ListView):
    model = Book
    template_name = 'html/shop-list.html'
    paginate_by = 24  # Số lượng items trên mỗi trang

    def get_queryset(self):
        queryset = Book.objects.filter(book_available=True)
        sort_by = self.request.GET.get('sort_by')

        if sort_by == 'name_asc':
            queryset = queryset.order_by('title')
        elif sort_by == 'name_desc':
            queryset = queryset.order_by('-title')
        elif sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        # Thêm các tùy chọn sắp xếp khác nếu cần

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', '')  # Giữ giá trị đã chọn của sắp xếp trong context
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            rating = form.cleaned_data['rating']
            user = request.user  # Assuming user is authenticated
            book = Book.objects.get(pk=book_id)
            comment = Comment.objects.create(book=book, user=user, content=content, rating=rating)
            comment.save()
            return redirect('detail', pk=book_id)
        else:
            context = self.get_context_data(**kwargs)
            context['comment_form'] = form
            return self.render_to_response(context)

class CommentUpdateView(LoginRequiredMixin,UpdateView):
    model = Comment
    fields = ['content', 'rating']
    template_name = 'detail.html'
    pk_url_kwarg = 'comment_id'
    
    def form_valid(self, form):
        form.save()
        return redirect('detail', pk=self.object.book.pk)

class CommentDeleteView(DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'detail.html'

    def get_success_url(self):
        book_id = self.object.book.pk
        return reverse_lazy('detail', kwargs={'pk': book_id})

class SearchResultsListView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        return Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))


class SemanticSearchResultsListView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        book_ids = semantic_search(query, books, vector, model)

        # Convert book IDs to a list of integers (assuming IDs are numeric)
        book_id_list = [int(book_id + 1) for book_id in book_ids]
        books_object = []
        for id in book_id_list:
            book = get_object_or_404(Book, id=id)
            books_object.append(book)
        # Filter Book objects by the retrieved IDs
        return books_object

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