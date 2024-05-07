'''import numpy as np
import pandas as pd
import ast
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity
books = pd.read_csv('C:/Users/HP/.vscode/Software-Engineering-83/Online Bookstore Test/Book dataset/Book_data.csv')
books= books[['isbn', 'title', 'series', 'genres', 'author', 'publisher','description','awards']]
books.dropna(inplace=True)
# we need to convert this string list to a list. For this we have a package ast
# literal_eval() function in ast helps in doing the job. i.e getting the literals out of the list

books['description'] = books['description'].apply(lambda x:x.split())
books['publisher'] = books['publisher'].str.split(',')
books['author'] = books['author'].str.split(',')
books['series'] = books['series'].str.split('#')
books['genres'] =books['genres'].str.split(',')
books['awards'] =books['awards'].str.split(',')
books['tags'] = books['description'] + books['genres'] + books['publisher'] + books['author'] + books['series'] + books['awards']
new_df = books[['isbn','title', 'tags']]
new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'].apply(lambda x:x.lower())

ps= PorterStemmer()
def stem(text):
  y = []

  for i in text.split():
    y.append(ps.stem(i))

  return " ".join(y)
new_df['tags'].apply(stem)

cv = CountVectorizer(max_features=10000,stop_words='english')
vector = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vector)
similarity[1]
def recommend(book):
  books_index = new_df[new_df['title'] ==book].index[0]
  distances = similarity[books_index]
  books_list = sorted(list(enumerate(distances)),reverse = True, key=lambda x:x[1])[1:6]

  for i in books_list:
    print(books.iloc[i[0]])
recommend('Twilight')'''
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import pickle

# Load the dataset
books = pd.read_csv('C:/Users/HP/.vscode/Software-Engineering-83/Online Bookstore Test/Book dataset/Book_data.csv')
books = books[['isbn', 'title', 'series', 'genres', 'author', 'publisher', 'description', 'awards']]
books.dropna(inplace=True)

# Combine relevant text columns into 'tags' for each book
books['tags'] = books['description'] + ' ' + books['genres'] + ' ' + books['publisher'] + ' ' + books['author'] + ' ' + books['series'] + ' ' + books['awards']

# Function to perform stemming on text
ps = PorterStemmer()
def stem_text(text):
    return ' '.join([ps.stem(word) for word in text.split()])

# Apply stemming to 'tags' column
books['tags'] = books['tags'].apply(stem_text)

# Initialize FrequencyVectorizer
cv = TfidfVectorizer(max_features=1500,stop_words='english')

# Fit and transform 'tags' to vectorized form
vector = cv.fit_transform(books['tags']).toarray()

# Calculate cosine similarity matrix
similarity = cosine_similarity(vector)
print(similarity)
def recommend(book_title):
    book_index = books[books['title'] == book_title].index[0]
    distances = similarity[book_index]
    # Get top 5 similar books (excluding the book itself)
    similar_books_indices = np.argsort(distances)[::-1][0:7]
    recommended_books = books.iloc[similar_books_indices][['title', 'author', 'description']]
    return recommended_books

# Test the recommendation function with a book title
recommendations = recommend('Harry Potter and the Order of the Phoenix')
print(recommendations)
with open('C:/Users/HP/.vscode/Software-Engineering-83/recommend_model.pkl', 'wb') as file:
    pickle.dump(similarity, file)
