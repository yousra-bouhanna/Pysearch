# Pysearch: Moteur de Recherche Personnalisé - Traitement du Langage Naturel (NLP)

## Présentation du projet
Ce projet a été réalisé dans le cadre du cours de programmation avec Python. Il s'agit d'un moteur de recherche personnalisé axé sur le thème du **Traitement du Langage Naturel (NLP)**. Le projet extrait et analyse des données issues de deux sources principales : **Reddit** et **ArXiv**. L'objectif est de permettre à l'utilisateur d'effectuer des recherches avancées, de comparer les deux corpus, et de visualiser les tendances et les éléments clés sous forme graphique.

## fonctionnalités principales
- **Recherche Classique**:
    Recherche par texte libre dans les deux corpus.

- **Recherche Avancée**
    Filtrage par :
    - Mots-clés
    - Date 
    - Auteur 
    - Source (Reddit ou ArXiv)

- **Comparaison des Corpus**
    Génération de nuages de mots :
    - Mots spécifiques à chaque corpus
    - Mots en commun entre les deux corpus

- **Analyse Temporelle**
    Tracé de graphes montrant l'évolution temporelle de la fréquence d'un mot :
    - Fréquence annuelle
    - Fréquence mensuelle

## Structure du projet


## Technologies utilisées
- Interface: streamlit
- Backend: Python

## Prérequis: 
Toutes les bibliothèques et dépendances nécessaires sont listées dans le fichier requirements.txt, situé à la racine du projet [requirements.txt](requirements.txt)

## Installation:
1. Clonez le projet :
    ```bash
    git clone https://github.com/yousra-bouhanna/Pysearch.git
    cd Pysearch

2. Créez et activez un environnement virtuel :
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Pour Unix
    .\.venv\Scripts\activate   # Pour Windows 

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt

4. Lancez l'application :
    ```bash
    streamlit run app.py


## Tests:
Des tests unitaires ont été mis en place pour valider le bon fonctionnement des différentes fonctionnalités du projet. Ils sont disponibles dans le répertoire [.github/Tests](.github/Tests) 

Vous pouvez executer les tests avec la commande:
    ```bash
    python -m unittest Tests/test_corpus.py


## Les contributeurs:

- [Yousra Bouhanna](https://github.com/yousra-bouhanna)
- [Mohamed Riad Sahrane](https://github.com/riadshrn)






