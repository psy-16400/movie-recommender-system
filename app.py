import streamlit as st
from recommender import load_data, create_similarity_matrix, get_recommendations
from collaborative_recommender import train_model, get_top_n_recommendations
from utils import fetch_movie_data_tmdb as fetch_movie_data

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.title("🎥 Movie Recommendation System")

movies = load_data()
similarity_matrix = create_similarity_matrix(movies)
model, ratings = train_model()

option = st.radio("Choose Recommendation Method:", ("Content-Based", "Collaborative Filtering"))

if option == "Content-Based":
    selected_movie = st.selectbox("Select a movie you like", movies['title'].values)
    if st.button("Recommend", key="cb"):
        recommendations = get_recommendations(selected_movie, movies, similarity_matrix)
        st.subheader("Top Recommendations:")
        cols = st.columns(2)
        for i, movie in enumerate(recommendations):
            data = fetch_movie_data(movie)
            if data:
                with cols[i % 2]:
                    if data.get('poster'):
                        st.image(data['poster'], width=150)
                    else:
                        st.write("No poster available.")
                    st.markdown(f"**[{data['title']}]({data['imdb_url']})**")
                    st.markdown(f"⭐ IMDb Rating: {data['rating']}/10")
                    
elif option == "Collaborative Filtering":
    user_ids = ratings['userId'].unique()
    selected_user = st.selectbox("Select a user ID", user_ids)
    if st.button("Recommend", key="cf"):
        recs = get_top_n_recommendations(int(selected_user), model, ratings)
        st.subheader("Top Recommendations:")
        cols = st.columns(2)
        for i, movie in enumerate(recs):
            data = fetch_movie_data(movie)
            with cols[i % 2]:
                if data:
                    st.image(data['poster'], width=150)
                    st.markdown(f"**[{data['title']}]({data['imdb_url']})**", unsafe_allow_html=True)
                else:
                    st.markdown(f"- {movie}")
