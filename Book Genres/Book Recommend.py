import numpy as np
import pandas as pd
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=10000,stop_words='english')
import nltk
from nltk.stem.porter import PorterStemmer
ps= PorterStemmer()
books = pd.read_csv('/content/goodreads_top100_from1980to2023_final.csv')
# genres
# id
# keywords
# title
# overview
# cast
# crew

books= books[['isbn', 'title', 'series_title', 'genres', 'authors', 'publisher','description']]
books.dropna(inplace=True)
books['description'] = books['description'].apply(lambda x:x.split())
books['publisher'] = books['publisher'].str.split(',')
books['authors'] = books['authors'].str.split(',')
books['series_title'] = books['series_title'].str.split('#')
books['genres'] =books['genres'].str.split(',')
books['tags'] = books['description'] + books['genres'] + books['publisher'] + books['authors'] + books['series_title']
new_df = books[['isbn','title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df.head()
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)
new_df['tags'] = new_df['tags'].apply(stem)
vector = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vector)
def recommend(book):
    books_index = new_df[new_df['title'] ==book].index[0]
    distances = similarity[books_index]
    books_list = sorted(list(enumerate(distances)),reverse = True, key=lambda x:x[1])[1:6]

    for i in books_list:
        print(new_df.iloc[i[0]])