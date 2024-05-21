from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.models import Book
from django.db.models import Q
from books.models import Comment,Cluster
from books.bookrecommendation import update_clusters
from django.contrib.auth.models import User
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
    book_ids = user_recommendation_list(request)
    manga_books_id = [3984, 3032, 3371,  2051, 6067, 8953, 1542]
    
    slider_books = Book.objects.filter(book_available=True)[406:412]
    new_arrivals = Book.objects.filter(book_available=True)[79:99]
    most_view_products = Book.objects.filter(book_available=True)[221:241]
    manga_books = Book.objects.filter(id__in= manga_books_id, book_available=True)

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
    
    nonfiction_bookss = Book.objects.filter(
    Q(genres__icontains='Nonfiction') & Q(book_available=True))[10:17]

    recommendbookss = Book.objects.filter(id__in = book_ids, book_available = True)

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
        'non_fiction_bookss': nonfiction_bookss,
        'biography_books': biography_bookss,
        'drama_bookss' : drama_bookss,
        'fantasy_bookss' : fantasy_bookss ,
        'fiction_bookss' : fiction_bookss,
        'history_bookss' : history_bookss , 
        'horror_bookss' : horror_bookss ,
        'magic_bookss' :    magic_bookss,
        'recommend_bookss' : recommendbookss,
        'romance_bookss' :   romance_bookss ,
        'magic_harry_potter_books': magic_harry_potter_books,
        'special_edition_books': special_edition_books,
        'manga_books' : manga_books}

    return render(request, 'index-2.html', context)

def shop_list(request):
    # Định nghĩa một truy vấn mới cho danh sách cửa hàng
    list_books = Book.objects.filter(book_available=True)[:20]  # Ví dụ: lấy 20 cuốn sách đầu tiên

    context = {'list_books': list_books}
    return render(request, 'html/shop-list.html', context)

@login_required
def user_recommendation_list(request):

    # get request user reviewed wines
    user_reviews = Comment.objects.filter(user_id=request.user.id)
    user_reviews_book_ids = set(map(lambda x: x.book_id, user_reviews))

    # get request user cluster name (just the first one righ now)
    #try:
     #   user_cluster_name = \
      #      User.objects.get(id=request.user.id).cluster_set.first().name
    #except: # if no cluster assigned for a user, update clusters
    update_clusters()
    user_cluster_name = User.objects.get(id=request.user.id).cluster_set.first().name

    # get usernames for other memebers of the cluster
    user_cluster_other_members = Cluster.objects.get(name=user_cluster_name).users.exclude(id=request.user.id).all()
    other_members_ids = set(map(lambda x: x.id, user_cluster_other_members))

    # get reviews by those users, excluding wines reviewed by the request user
    other_users_reviews = \
        Comment.objects.filter(user_id__in=other_members_ids) \
            .exclude(book__id__in=user_reviews_book_ids)
    other_users_reviews_book_ids = set(map(lambda x: x.book_id, other_users_reviews))

    # then get a wine list including the previous IDs, order by rating
    return other_users_reviews_book_ids
    #book_list = sorted(
     #   list(Book.objects.filter(id__in=other_users_reviews_book_ids)),
      #  key=lambda x: x.rating,
       # reverse=True
    #)