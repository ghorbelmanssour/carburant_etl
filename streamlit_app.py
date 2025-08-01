# streamlit_app.py

import streamlit as st
import pandas as pd
import psycopg2
from config.config import DB_CONFIG

st.set_page_config(page_title="Prix des carburants", layout="wide")
st.title("⛽ Visualisation des prix des carburants (depuis PostgreSQL)")

@st.cache_data(ttl=600)
def get_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = "SELECT * FROM prix_carburants"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Connexion échouée à PostgreSQL.\nDétail : {str(e)}")
        return pd.DataFrame()

df = get_data()

if df.empty:
    st.warning("Aucune donnée disponible.")
else:
    # Filtres
    villes = sorted(df["ville"].dropna().unique())
    carburants = sorted(df["carburant"].dropna().unique())

    selected_ville = st.selectbox("📍 Ville", ["Toutes"] + villes)
    selected_carburant = st.selectbox("⛽ Carburant", ["Tous"] + carburants)

    filtered_df = df.copy()
    if selected_ville != "Toutes":
        filtered_df = filtered_df[filtered_df["ville"] == selected_ville]
    if selected_carburant != "Tous":
        filtered_df = filtered_df[filtered_df["carburant"] == selected_carburant]

    st.metric("Nombre de stations", len(filtered_df["station_id"].unique()))
    st.dataframe(filtered_df)

    # Affichage prix moyen dans le temps
    df["date_maj"] = pd.to_datetime(df["date_maj"])
    evolution = filtered_df.groupby("date_maj")["prix"].mean()
    st.line_chart(evolution, use_container_width=True)