import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    return pd.read_csv('data/movies.csv')

def create_similarity_matrix(movies):
    tfidf = TfidfVectorizer(stop_words='english')
    movies['genres'] = movies['genres'].fillna('')
    tfidf_matrix = tfidf.fit_transform(movies['genres'])
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(title, movies, similarity_matrix):
    idx = movies[movies['title'].str.lower() == title.lower()].index
    if idx.empty:
        return []
    idx = idx[0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    return movies['title'].iloc[[i[0] for i in sim_scores]].tolist()
