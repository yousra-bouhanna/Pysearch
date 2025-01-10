import streamlit as st
import pandas as pd
from Modules.corpus import Corpus
from Modules.searchEngine import SearchEngine
from Modules.corpus import compare
from wordcloud import WordCloud
import os
import pickle
import matplotlib.pyplot as plt
from tabulate import tabulate
import re

# Initialisation de l'application Streamlit
st.set_page_config(page_title="Moteur de recherche", layout="wide")
st.title("Moteur de recherche sur les documents")

@st.cache_resource
def load_pkl(file):
    """
    Charge un fichier .pkl.

    Args:
        file: Fichier téléchargé (Streamlit UploadedFile).

    Returns:
        L'objet désérialisé du fichier .pkl.
    """
    try:
        return pickle.load(file)
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier .pkl : {e}")
        return None


def load_corpus_from_sidebar():
    """
    Fonction pour gérer le chargement d'un fichier .pkl depuis le dossier Data ou depuis la machine de l'utilisateur.

    Returns:
        Corpus: Objet Corpus chargé ou None si aucun fichier n'est sélectionné ou valide.
    """
    st.sidebar.header("Chargement du corpus")

    # Option pour charger depuis Data ou la machine
    default_directory = "Data"
    load_mode = st.sidebar.radio("Mode de chargement :", ["Depuis Data", "Depuis votre machine"])

    corpus = None

    if load_mode == "Depuis Data":
        if os.path.exists(default_directory):
            pkl_files = [f for f in os.listdir(default_directory) if f.endswith(".pkl")]
            if pkl_files:
                selected_file = st.sidebar.selectbox("Sélectionnez un fichier .pkl :", pkl_files)
                corpus_path = os.path.join(default_directory, selected_file)
                st.sidebar.write(f"Fichier sélectionné : {selected_file}")
                corpus = load_pkl(open(corpus_path, "rb"))
            else:
                st.sidebar.error("Aucun fichier .pkl disponible dans le dossier 'Data'.")
        else:
            st.sidebar.error(f"Le dossier '{default_directory}' n'existe pas.")
    elif load_mode == "Depuis votre machine":
        corpus_file = st.sidebar.file_uploader("Choisissez un fichier .pkl :", type=["pkl"])
        if corpus_file:
            corpus = load_pkl(corpus_file)

    return corpus

def load_two_corpora_from_sidebar(default_directory="Data"):
    """
    Gère le chargement de deux corpus depuis le dossier 'Data' ou via l'interface de l'utilisateur.

    Args:
        default_directory (str): Chemin du dossier contenant les fichiers `.pkl` par défaut.

    Returns:
        tuple: Deux objets Corpus ou None si l'un ou les deux ne sont pas valides.
    """
    st.sidebar.header("Comparer deux corpus")

    # Mode de chargement pour chaque corpus
    load_mode_corpus1 = st.sidebar.radio("Mode de chargement pour le premier corpus:", ["Depuis Data", "Depuis votre machine"], key="mode1")
    load_mode_corpus2 = st.sidebar.radio("Mode de chargement pour le deuxième corpus:", ["Depuis Data", "Depuis votre machine"], key="mode2")

    corpus1, corpus2 = None, None

    # Charger le premier corpus
    if load_mode_corpus1 == "Depuis Data" and os.path.exists(default_directory):
        pkl_files = [f for f in os.listdir(default_directory) if f.endswith(".pkl")]
        if pkl_files:
            selected_file1 = st.sidebar.selectbox("Sélectionnez le premier fichier .pkl :", pkl_files, key="corpus1")
            corpus1 = load_pkl(open(os.path.join(default_directory, selected_file1), "rb"))
        else:
            st.sidebar.error("Aucun fichier .pkl trouvé dans le dossier 'Data'.")
    elif load_mode_corpus1 == "Depuis votre machine":
        corpus1_file = st.sidebar.file_uploader("Chargez le premier fichier .pkl :", type=["pkl"], key="corpus1_file")
        if corpus1_file:
            corpus1 = load_pkl(corpus1_file)

    # Charger le deuxième corpus
    if load_mode_corpus2 == "Depuis Data" and os.path.exists(default_directory):
        pkl_files = [f for f in os.listdir(default_directory) if f.endswith(".pkl")]
        if pkl_files:
            selected_file2 = st.sidebar.selectbox("Sélectionnez le deuxième fichier .pkl :", pkl_files, key="corpus2")
            corpus2 = load_pkl(open(os.path.join(default_directory, selected_file2), "rb"))
        else:
            st.sidebar.error("Aucun fichier .pkl trouvé dans le dossier 'Data'.")
    elif load_mode_corpus2 == "Depuis votre machine":
        corpus2_file = st.sidebar.file_uploader("Chargez le deuxième fichier .pkl :", type=["pkl"], key="corpus2_file")
        if corpus2_file:
            corpus2 = load_pkl(corpus2_file)

    return corpus1, corpus2


# Fonction pour générer un nuage de mots
def plot_wordcloud(words, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')
    st.pyplot(plt)
    plt.close()


def clean_dataframe(df):
    """
    Nettoie les colonnes d'un DataFrame en supprimant les retours à la ligne
    et les tabulations des chaînes de caractères.
    """
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = df[column].apply(lambda x: str(x).replace('\n', ' ').replace('\t', ' ') if pd.notnull(x) else x)
    return df