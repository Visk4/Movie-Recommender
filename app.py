import streamlit as st
import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# API Calls
def fetch_movie_details(movieid):
    details = requests.get(
        f"https://api.themoviedb.org/3/movie/{movieid}?api_key={API_KEY}&language=en-US"
    ).json()
    credits = requests.get(
        f"https://api.themoviedb.org/3/movie/{movieid}/credits?api_key={API_KEY}"
    ).json()
    external = requests.get(
        f"https://api.themoviedb.org/3/movie/{movieid}/external_ids?api_key={API_KEY}"
    ).json()
    return details, credits, external

def fetch_poster(movieid):
    details, _, _ = fetch_movie_details(movieid)
    poster_path = details.get("poster_path")
    return "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else ""

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies["title"].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

# URL Query
query_params = st.query_params
movieid_param = query_params.get("movie_id", None)

# Show Detail Page
if movieid_param:
    details, credits, external = fetch_movie_details(movieid_param)
    poster_url = "https://image.tmdb.org/t/p/w500/" + details.get('poster_path', '')

    st.image(poster_url, width=300)
    st.markdown(f"## {details.get('title')}")
    st.markdown(f"**📅 Release Date:** {details.get('release_date')}")
    st.markdown(f"**⭐ Rating:** {details.get('vote_average')} / 10")
    st.markdown(f"**📝 Overview:** {details.get('overview')}")
    
    # Extract cast and director
    cast_list = [c['name'] for c in credits.get('cast', [])[:4]]
    director = next((crew['name'] for crew in credits.get('crew', []) if crew['job'] == 'Director'), 'N/A')
    st.markdown(f"**🎬 Director:** {director}")
    st.markdown("**🎭 Cast:** " + ", ".join(cast_list))

    # IMDb Link
    imdb_id = external.get('imdb_id', None)
    if imdb_id:
        imdb_url = f"https://www.imdb.com/title/{imdb_id}"
        st.markdown(f"[🔗 View on IMDb]({imdb_url})", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔙 Back to Recommender"):
        st.query_params.clear()
        st.rerun()

# Show Recommender Interface
else:
    st.title("🎬 Content-Based Movie Recommender System")
    selected_movie_name = st.selectbox("Choose a movie you like:", movies_list)

    def recommend(movie):
        movie_ind = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_ind]
        similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended = []
        for i in similar_movies:
            movie_title = movies.iloc[i[0]].title
            movie_id = movies.iloc[i[0]].movie_id
            recommended.append((movie_title, movie_id))
        return recommended

    if st.button("🎥 Recommend"):
        st.session_state.recommendations = recommend(selected_movie_name)

    if "recommendations" in st.session_state:
        cols = st.columns(5)
        for idx, (name, movieid) in enumerate(st.session_state.recommendations):
            with cols[idx]:
                poster_url = fetch_poster(movieid)
                st.markdown(
                    f"""
                    <a href='?movie_id={movieid}'>
                        <img src='{poster_url}' width='150px' style='border-radius:10px'/>
                    </a>
                    <div style='text-align:center; font-weight:bold; margin-top:5px'>{name}</div>
                    """,
                    unsafe_allow_html=True
                )
