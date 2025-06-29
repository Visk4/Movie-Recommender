# Movie-Recommender

# 🎬 Movie Recommender System

This is a Content-Based Movie Recommender System built with **Streamlit** that suggests similar movies based on your selection. It uses a precomputed similarity matrix and movie metadata to provide recommendations along with poster previews and additional information.

---

## 📌 Features

- 🔍 **Content-based filtering** using cosine similarity
- 🖼️ Shows **movie posters**
- 🎭 Displays **cast and director info**
- 🌐 Clickable **IMDb** and **TMDB** links
- 📱 Responsive, Streamlit-based web UI

---

## 🧠 How It Works

1. Loads a list of movies and a similarity matrix (`similarity.pkl`)
2. When you select a movie, it:
   - Finds the most similar movies based on content features
   - Fetches movie details via TMDB API
3. Displays:
   - Movie title and poster
   - Cast, director, overview
   - External links

---
