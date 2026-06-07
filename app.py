import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

TMDB_API_KEY = '8265bd1679663a7ea12ac168da84d2e8'

def fetch_poster(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
        response = requests.get(url)
        data = response.json()
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass
    return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommendations = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        score = round(i[1] * 100, 1)
        poster = fetch_poster(title)
        recommendations.append({'title': title, 'score': score, 'poster': poster})
    return recommendations

st.markdown("""
    <h1 style='text-align: center;'>🎬 Movie Recommender System</h1>
    <p style='text-align: center; color: gray;'>Powered by Content-Based Filtering & Cosine Similarity</p>
    <br>
""", unsafe_allow_html=True)

selected_movie = st.selectbox('Select a movie you like', movies['title'].values)

if st.button('🔍 Get Recommendations', use_container_width=True):
    with st.spinner('Finding similar movies...'):
        recommendations = recommend(selected_movie)
    
    st.subheader(f"Because you liked **{selected_movie}**:")
    cols = st.columns(5)
    
    for idx, rec in enumerate(recommendations):
        with cols[idx]:
            if rec['poster']:
               st.image(rec['poster'], width=300)
            else:
                st.markdown("🎬")
            st.markdown(f"**{rec['title']}**")
            st.markdown(f"Match: `{rec['score']}%`")
# Large files
similarity.pkl
movies.pkl

# CSV data files
*.csv

# Environment
.env
venv/
env/
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo

# Jupyter checkpoints
.ipynb_checkpoints/

# VS Code
.vscode/