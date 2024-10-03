import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("mymoviedb.csv")

def movies_for_genre(data,genre):
    data['Vote_Count'] = pd.to_numeric(data['Vote_Count'],errors='coerce') 
    data = data.dropna(subset=['Vote_Count'])
    preprocessed_data = data[(data['Genre'].str.contains(genre, case=False, na=False)) & (data['Vote_Count'] > 5000)]
    sorted_data = preprocessed_data.sort_values(by='Vote_Count', ascending=False)
    return sorted_data.head(10)
def main():
    st.title("Collaborative Filtering Recommendation System for Movies")
    data = load_data()
    data['Genre'] = data['Genre'].fillna('').astype(str)
    genres = set([g.strip() for sublist in data['Genre'].str.split(',') for g in sublist if isinstance(g, str) and g.strip()])
    selected_genre = st.selectbox("Select a Genre", sorted(genres))
    if selected_genre:
        top_movies = movies_for_genre(data, selected_genre)
        if not top_movies.empty:
            st.write(f"### Top 10 Movies in {selected_genre} with more than 5000 votes")
            for index, row in top_movies.iterrows():
                st.write(f"**Title:** {row['Title']}")
                st.write(f"**Overview:** {row['Overview']}")
                st.write(f"**Vote Count:** {row['Vote_Count']}")
                if pd.notna(row['Poster_Url']) and row['Poster_Url'].startswith('http'):
                    st.image(row['Poster_Url'])
                st.write("")
        else:
            st.write("No movies found with more than 5000 votes in this genre.")

if __name__ == "__main__":
    main()
