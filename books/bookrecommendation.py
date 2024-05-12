import pickle
import pandas as pd
import numpy as np
from nltk.stem.porter import PorterStemmer
ps= PorterStemmer()
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
# Load the model from the .pkl file
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
with open('vector.pkl', 'rb') as file:
    vector = pickle.load(file)
# Function to recommend similar books
conn = sqlite3.connect('C:/Users/HP/.vscode/Software-Engineering-83/db.sqlite3')
query = "SELECT * FROM books_book;"
books = pd.read_sql_query(query, conn)
conn.close()
def recommend(book_title):
    book_index = books[books['title'] == book_title].index[0]
    similarity = cosine_similarity(vector)
    distances = similarity[book_index]
    # Get top 5 similar books (excluding the book itself)
    similar_books_indices = np.argsort(distances)[::-1][1:7]
    recommended_books = books.iloc[similar_books_indices][['title', 'author', 'description']]
    return recommended_books

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
    return ranked_indices

# Test the recommendation function with a book title

print(semantic_search('knights fighting , civil wars, thrones',books,vector,model))
