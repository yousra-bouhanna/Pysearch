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


# Menu principal
menu = st.sidebar.selectbox("Menu", ["Accueil", "Charger un corpus", "Analyse du corpus"])

if menu == "Accueil":
    st.header("Bienvenue dans le moteur de recherche sur les documents !")
    st.write("Explorez les fonctionnalités disponibles via le menu à gauche.")

    st.subheader("Fonctionnalités disponibles")
    
    st.markdown("### 1. Charger un corpus")
    st.write("- **Entrée** : Fichier `.pkl` contenant un corpus.")
    st.write("- **Sortie** : Visualisation des métadonnées du corpus, comme le nombre de documents et d'auteurs.")
    st.write("Cette section vous permet de charger un fichier corpus au format `.pkl` pour l'utiliser dans d'autres fonctionnalités.")

    st.markdown("### 2. Analyse du corpus")
    st.write("- **Entrée** : Fichier `.pkl` contenant un corpus.")
    st.write("- **Sortie** :")
    st.write("  -- Visualisation du contenu des documents.")
    st.write("  -- Statistiques par auteur, incluant le nombre de documents et la taille moyenne des textes.")
    st.write("  -- Liste des mots les plus utilisés et le nombre de documents contenant chaque mot.")
    st.write("Cette section vous aide à explorer les détails et les statistiques globales du corpus.")

    st.markdown("### 3. Moteur de recherche avancé")
    st.write("- **Entrée** :")
    st.write(" -- Une requête textuelle (mot-clé ou phrase).")
    st.write("  -- Un fichier `.pkl` contenant un corpus.")
    st.write("- **Sortie** :")
    st.write("  -- Liste des documents pertinents triés par similarité.")
    st.write("  -- Passages pertinents (seulement qui sont vraiment similaires) contenant les mots de la requête.")
    st.write("Cette section vous permet de rechercher des documents pertinents à partir d'une requête.")

elif menu == "Charger un corpus":
    st.header("Charger un corpus depuis un fichier Pickle")
    corpus = load_corpus_from_sidebar()

    # Afficher les détails du corpus chargé
    if corpus:
        if isinstance(corpus, Corpus):
            st.success("Corpus chargé avec succès !")
            st.write(f"Nom du corpus : {corpus.nom}")
            st.write(f"Nombre total de documents : {corpus.ndoc}")
            st.write(f"Nombre total d'auteurs : {corpus.naut}")
            st.subheader("Documents disponibles")
            st.write(pd.DataFrame([{ 
                "Titre": doc.titre, 
                "Auteur": ", ".join(doc.auteur) if isinstance(doc.auteur, list) else str(doc.auteur), 
                "Date": doc.date 
            } for doc in corpus.id2doc.values()]))
        else:
            st.error("Le fichier chargé n'est pas un corpus valide.")


elif menu == "Analyse du corpus":
    st.header("Analyse du corpus")
    corpus = load_corpus_from_sidebar()

    if corpus:
        if isinstance(corpus, Corpus):
            st.success("Corpus chargé avec succès !")

            # Afficher le contenu du corpus
            st.subheader("Contenu du corpus")
            st.write(pd.DataFrame([{ 
                "Titre": doc.titre, 
                "Auteur": ", ".join(doc.auteur) if isinstance(doc.auteur, list) else str(doc.auteur), 
                "Date": doc.date 
            } for doc in corpus.id2doc.values()]))
            # Sélection d'un auteur et affichage de ses stats
            st.subheader("Statistiques par auteur")
            authors = list(corpus.authors.keys())
            selected_author = st.selectbox("Sélectionnez un auteur:", authors)
            if selected_author:
                author_stats = corpus.authors[selected_author].stats()
                st.write(f"Statistiques pour {selected_author}:")
                st.write(author_stats)

            # Mots les plus utilisés et Nombre de documents par mot
            st.subheader("Mots les plus utilisés & Nombre de documents par mot")

            try:
                word_doc_freq = corpus.nbr_documents()
                # Trier les données
                word_doc_freq_sorted = word_doc_freq.sort_values(by="nbr_occurence", ascending=False)

                # Afficher les données triées
                st.dataframe(word_doc_freq_sorted)

            except Exception as e:
                st.error(f"Une erreur est survenue lors du calcul ou de l'affichage : {e}")

        else:
            st.error("Le fichier chargé n'est pas un corpus valide.")


elif menu == "Moteur de recherche":
    st.header("Moteur de recherche avancé")
    corpus = load_corpus_from_sidebar()

    if corpus:
        if isinstance(corpus, Corpus):
            st.success("Corpus chargé avec succès !")
            search_engine = SearchEngine(corpus)

            query = st.text_input("Entrez votre requête pour la recherche avancée:")
            top_n = st.slider("Nombre de résultats à afficher:", min_value=1, max_value=20, value=5)

            if st.button("Lancer la recherche") and query:
                results = search_engine.search_motor(query, top_n)

                if not results.empty:
                    st.subheader("Résultats de la recherche")
                    for _, row in results.iterrows():
                        st.markdown(f"### {row['titre']}")
                        st.markdown(f"**Auteur(s)**: {row['auteur']}")
                        st.markdown(f"**Date**: {row['date']}")
                        st.markdown(f"**Score de similarité**: {row['similarité']:.2f}")
                        st.markdown(f"**URL**: [Lien]({row['url']})")
                        st.markdown(f"**Nombre de passages trouvés**: {len(row['passages'])}")
                        if row['passages']:
                            st.markdown("#### Passages pertinents:")
                            for passage in row['passages']:
                                st.markdown(f"- {passage}")
                        st.markdown("---")
                else:
                    st.write("Aucun résultat trouvé.")
        else:
            st.error("Le fichier chargé n'est pas un corpus valide.")