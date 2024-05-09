import pickle
import pandas as pd
import numpy as np
from django.contrib.auth.models import User
from .models import Book
# Load the model from the .pkl file
with open('recommend_model.pkl', 'rb') as file:
    similarity = pickle.load(file)
# Function to recommend similar books
books = pd.read_csv('C:/Users/HP/.vscode/Software-Engineering-83/Online Bookstore Test/Book dataset/Book_data.csv')
books = books[['isbn', 'title', 'series', 'genres', 'author', 'publisher', 'description', 'awards']]
def recommend(book_title):
    book_index = books[books['title'] == book_title].index[0]
    distances = similarity[book_index]
    # Get top 5 similar books (excluding the book itself)
    similar_books_indices = np.argsort(distances)[::-1][1:7]
    recommended_books = books.iloc[similar_books_indices][['title', 'author', 'description']]
    return recommended_books

# Test the recommendation function with a book title
user_instance = User.objects.get(user_id='1')
wishlist_books = user_instance.user_wishlist.all()
recommendations = recommend(wishlist_books[:-1])
print(recommendations)
