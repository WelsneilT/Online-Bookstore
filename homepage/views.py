from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.models import Book
from django.db.models import Q
import pickle
import pandas as pd
import numpy as np
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

ps= PorterStemmer()

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
def recommend(book_id):
    #book_index = books[books['title'] == book_title].index[0]
    similarity = cosine_similarity(vector)
    distances = similarity[book_id - 1]
    # Get top 5 similar books (excluding the book itself)
    similar_books_indices = np.argsort(distances)[::-1][1:21]
    recommended_books = books.iloc[similar_books_indices][['title', 'author']]
    print(recommended_books)
    return similar_books_indices

def get_book_ids_of_current_user(request):
    current_user = request.user

    # Filter Book objects in the current user's wishlist
    wishlist_books = Book.objects.filter(users_wishlist=current_user)

    # Access book_id values from the join table (book_user_wishlist)
    book_ids = list(wishlist_books.values_list('id', flat=True))

    return book_ids

@login_required
def home(request):
    user_wishlist_id = get_book_ids_of_current_user(request)
    if len(user_wishlist_id) != 0 and user_wishlist_id[-1] < 10000 :
        list = recommend(user_wishlist_id[-1])
        print(list)
        book_id_list = [int(id + 1) for id in list]    
        featured_products = Book.objects.filter(id__in=book_id_list)
    else:
        featured_products = Book.objects.filter(book_available=True)[10020:10040]
    slider_books = Book.objects.filter(book_available=True)[406:412]
    new_arrivals = Book.objects.filter(book_available=True)[79:99]
    most_view_products = Book.objects.filter(book_available=True)[221:241]

    adventure_books = Book.objects.filter(
    Q(genres__icontains='Adventure') & Q(book_available=True))[310:320]
    special_offers = Book.objects.filter(book_available=True)[3983:3984]
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
    Q(genres__icontains='Nonfiction') & Q(book_available=True))[10:17]
    romance_bookss = Book.objects.filter(
    Q(genres__icontains='Romance') & Q(book_available=True))[510:520]
    magic_harry_potter_books = Book.objects.filter(
    Q(genres__icontains='Magic') & Q(title__icontains='Harry Potter') & Q(book_available=True))[0:20]
    special_edition_books = Book.objects.filter(
    Q(author__icontains='Yana Toboso') & Q(book_available=True))[0:17]

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

def shop_list(request):
    # Định nghĩa một truy vấn mới cho danh sách cửa hàng
    list_books = Book.objects.filter(book_available=True)[:20]  # Ví dụ: lấy 20 cuốn sách đầu tiên

    context = {'list_books': list_books}
    return render(request, 'html/shop-list.html', context)

def basket_hover(request):
    basket = Basket(request)
    basket_json = []
    total_price = 0

    for item in basket.__iter__():
    # Convert Decimal objects to strings
        item['price'] = str(item['price'])
        item['total_price'] = str(item['total_price'])
    # Extract relevant information from Book objects
        book_info = {
            'id': item['product'].id,
            'title': item['product'].title,
            'author': item['product'].author,
            'description': item['product'].description,
            'price': float(item['product'].price),  # Convert to string if needed
            'image_url': item['product'].image_url,
            'book_available': item['product'].book_available,
            'pk':item['product'].pk,
            # Add other relevant fields as needed
        }
        item['product'] = book_info

        basket_json.append(item)
    total_price = basket.get_total_price()  # Calculate total price

    return render(request, 'home', {'basket': basket, 'total_price': total_price})
