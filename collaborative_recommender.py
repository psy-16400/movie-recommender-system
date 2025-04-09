from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import pandas as pd

def train_model():
    ratings = pd.read_csv('data/ratings.csv')
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
    trainset, _ = train_test_split(data, test_size=0.2, random_state=42)
    model = SVD()
    model.fit(trainset)
    return model, ratings

def get_top_n_recommendations(user_id, model, ratings, n=10):
    movie_ids = ratings['movieId'].unique()
    watched = ratings[ratings['userId'] == user_id]['movieId']
    unseen = [m for m in movie_ids if m not in watched.values]
    predictions = [(movie_id, model.predict(user_id, movie_id).est) for movie_id in unseen]
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_movie_ids = [movie_id for movie_id, _ in predictions[:n]]
    movies_df = pd.read_csv('data/movies.csv')
    return movies_df[movies_df['movieId'].isin(top_movie_ids)]['title'].tolist()
