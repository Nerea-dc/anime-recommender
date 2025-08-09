
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# -----------------------
# Cargar datos y modelo
# -----------------------
@st.cache_resource
def cargar_modelos():
    df_model = pd.read_pickle("df_model.pkl")
    df_original = pd.read_pickle("df_original.pkl")
    X_latent_deep = np.load("X_latent_deep.npy")
    with open("knn_deep.pkl", "rb") as f:
        knn_deep = pickle.load(f)
    return df_model, df_original, X_latent_deep, knn_deep

df_model, df_original, X_latent_deep, knn_deep = cargar_modelos()

# -----------------------
# Función de recomendación
# -----------------------
def get_recommendations(anime_id):
    anime_idx = df_model[df_model['anime_id'] == anime_id].index[0]
    anime_vector = X_latent_deep[anime_idx].reshape(1, -1)
    _, kneighbors_idx = knn_deep.kneighbors(anime_vector)

    kneighbors_anime_ids = df_model.loc[kneighbors_idx[0], 'anime_id'].tolist()
    df_kneighbors = df_original[df_original['anime_id'].isin(kneighbors_anime_ids)].copy()
    df_kneighbors['anime_id'] = pd.Categorical(df_kneighbors['anime_id'], categories=kneighbors_anime_ids, ordered=True)
    df_kneighbors = df_kneighbors.sort_values('anime_id').reset_index(drop=True)
    return df_kneighbors

# -----------------------
# Interfaz Streamlit
# -----------------------
st.title("🎌 Recomendador de animes 🎌")
st.markdown("Descubre nuevos animes basados en tus gustos. Este sistema utiliza un modelo de **Deep Autoencoder combinado con KNN** para recomendarte 20 animes similares al que elijas.")

# Entrada de texto libre para búsqueda parcial
query = st.text_input("Escribe una palabra clave del nombre del anime que te haya gustado:")

# Filtrar opciones que contienen el texto (ignorando mayúsculas)
if query:
    anime_ids = df_original[df_original['name'].str.contains(query, case=False, na=False)][['anime_id', 'name']].drop_duplicates().sort_values('name')
    if anime_ids.empty:
        st.warning("No se encontraron animes con ese nombre.")
        st.stop()
else:
    anime_ids = df_original[['anime_id', 'name']].drop_duplicates().sort_values('name')

# Crear diccionario y seleccionar anime
anime_dict = dict(zip(anime_ids['name'], anime_ids['anime_id']))
anime_name = st.selectbox("Elige el anime base para obtener recomendaciones:", options=anime_dict.keys())
selected_anime_id = anime_dict[anime_name]

# Obtener recomendaciones
df_kneighbors = get_recommendations(selected_anime_id)

# Mostrar anime consultado
anime = df_kneighbors.iloc[0]
st.markdown(f"### Recomendaciones basadas en: [{anime['name']}]({anime['anime_url']}) (ID: {anime['anime_id']})")
st.image(anime['image_url'], width=150)
score = f"{anime['score']:.2f}" if pd.notnull(anime['score']) else "N/D"
votos = f"{int(anime['scored_by']):,}" if pd.notnull(anime['scored_by']) else "N/D"
rating = anime['rating'] if pd.notnull(anime['rating']) else "N/D"
ranking = f"{int(anime['rank'])}" if pd.notnull(anime['rank']) else "N/D"
st.caption(f"🏆 Ranking: {ranking} | 💯 Puntuación: {score} (votos: {votos}) | 🔞 Clasificación: {rating}")

# Mostrar animes recomendados
st.markdown("### Animes recomendados:")

# Dividir por estado de emisión
df_estrenados = df_kneighbors[df_kneighbors['upcoming'] == 0].iloc[1:]
df_upcoming = df_kneighbors[df_kneighbors['upcoming'] == 1]

col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Ya estrenados")
    for i, row in df_estrenados.iterrows():
        st.markdown(f"**{i}. [{row['name']}]({row['anime_url']}) (ID: {row['anime_id']})**")
        st.image(row['image_url'], width=120)
        score = f"{row['score']:.2f}" if pd.notnull(row['score']) else "N/D"
        votos = f"{int(row['scored_by']):,}" if pd.notnull(row['scored_by']) else "N/D"
        rating = row['rating'] if pd.notnull(row['rating']) else "N/D"
        ranking = f"{int(row['rank'])}" if pd.notnull(row['rank']) else "N/D"
        st.caption(f"🏆 Ranking: {ranking} | 💯 Puntuación: {score} (votos: {votos}) | 🔞 Clasificación: {rating}")
        st.markdown("---")


with col2:
    st.subheader("🎬 Próximos estrenos")
    if df_upcoming.empty:
        st.info("No hay recomendaciones que estén por estrenar.")
    for i, row in df_upcoming.iterrows():
        st.markdown(f"**{i}. [{row['name']}]({row['anime_url']}) (ID: {row['anime_id']})**")
        st.image(row['image_url'], width=120)
        score = f"{row['score']:.2f}" if pd.notnull(row['score']) else "N/D"
        votos = f"{int(row['scored_by']):,}" if pd.notnull(row['scored_by']) else "N/D"
        rating = row['rating'] if pd.notnull(row['rating']) else "N/D"
        ranking = f"{int(row['rank'])}" if pd.notnull(row['rank']) else "N/D"
        st.caption(f"🏆 Ranking: {ranking} | 💯 Puntuación: {score} (votos: {votos}) | 🔞 Clasificación: {rating}")
        st.markdown("---")
