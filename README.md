# Pysearch 🔍

**Moteur de Recherche Personnalisé** axé sur le **Traitement du Langage Naturel (NLP)**, conçu pour analyser et comparer des corpus issus de **Reddit** et **ArXiv**. Avec des fonctionnalités avancées comme la recherche filtrée, la comparaison de corpus, et l'analyse temporelle, Pysearch est un outil puissant pour explorer et visualiser des données textuelles.

---


## 📁 Structure du Projet
```bash
Pysearch/
├── Data/                      # Données utilisées dans le projet
│   ├── ArXiv_corpus.pkl
│   ├── Arxiv_data.csv
│   │       .
│   └── Reddit_corpus.pkl
├── Modules/                   # Modules Python (Core logic)
│   ├── __init__.py
│   ├── author.py
│   ├── corpus.py
│   ├── document.py
│   ├── documentFactory.py
│   └── searchEngine.py
├── Outputs/                   # Fichiers générés (Ex. Nuages de mots)
│   ├── Common words.png
│   ├── Unique words in corpus.png
│   └── Unique words in discours.png
├── Tests/                     # Scripts pour les tests unitaires
│   ├── __init__.py
│   └── test_corpus.py
├── Tools/                     # Outils et scripts annexes
│   ├── interface.ipynb
│   └── main.py
├── .gitignore                 # Fichiers à ignorer par Git
├── app.py                     # Script principal de l'application Streamlit
├── Corpora.py                 # Script supplémentaire pour gérer les corpus
├── README.md                  # Documentation du projet
└── requirements.txt           # Liste des dépendances Python

```

--- 

## 🚀 Technologies Utilisées

### Frontend
- ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=streamlit&logoColor=white) **Streamlit**

### Backend
- ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) **Python**
- ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white) **Pandas** : Analyse et manipulation des données.
- ![NumPy](https://img.shields.io/badge/-NumPy-013243?logo=numpy&logoColor=white) **NumPy** : Calcul numérique pour les matrices et vecteurs.
- ![Scikit-learn](https://img.shields.io/badge/-Scikit--learn-F7931E?logo=scikit-learn&logoColor=white) **Scikit-learn** : Similarité cosinus.

### Visualisation
- ![Matplotlib](https://img.shields.io/badge/-Matplotlib-11557C?logo=matplotlib&logoColor=white) **Matplotlib** : Création de graphiques et visualisations.
- ![WordCloud](https://img.shields.io/badge/-WordCloud-009688?logo=wordcloud&logoColor=white) **WordCloud** : Génération de nuages de mots.

### Gestion des Données
- ![Pickle](https://img.shields.io/badge/-Pickle-FFCC00?logo=python&logoColor=black) **Pickle** : Sérialisation et désérialisation des corpus au format `.pkl`.

---

## 🚀 Fonctionnalités Principales

### 🔍 **Moteur de Recherche**
Effectuez des recherches sur des corpus textuels avec deux approches :
- **Recherche Classique** : Recherche textuelle avec TF-IDF.
- **Recherche Avancée** :
  - Par **mot-clé** : Analyse sémantique des textes.
  - Par **auteur** : Filtrage des documents par créateur.
  - Par **date** : Recherche basée sur la période.
  - Par **source** : Filtrage selon l'origine des données (Reddit ou ArXiv).

### 📊 **Comparaison de Corpus**
Identifiez les similarités et différences entre deux corpus :
- Mots en commun.
- Mots spécifiques à chaque corpus.
- Nuages de mots interactifs pour une meilleure visualisation.

### 📈 **Analyse Temporelle**
Visualisez l'évolution de la fréquence des mots clés :
- Analyse mensuelle ou annuelle.
- Graphiques dynamiques.

### 🛠️ **Analyse du Corpus**
Obtenez des statistiques détaillées :
- Liste des documents.
- Mots les plus utilisés.
- Fréquence des documents contenant chaque mot.



---

## 📄 Instructions d'Installation

### Prérequis
- Python 3.10+
- `pip` pour la gestion des dépendances.

---

### Étapes d'installation

1.  Clonez le dépôt Git :
    ```bash
    git clone https://github.com/yousra-bouhanna/Pysearch.git
    cd Pysearch
    ```

2.  Créez et activez un environnement virtuel :
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Pour Unix
    .\.venv\Scripts\activate   # Pour Windows
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

4. Lancez l'application :
    ```bash
    streamlit run app.py
    ```

---

## 🧪 Tests Unitaires

### Commande pour exécuter les tests :
```bash
python -m unittest Tests/test_corpus.py
```

- Des tests unitaires ont été mis en place pour valider le bon fonctionnement des différentes fonctionnalités du projet.

---

## 👥 Contributeurs

- [Yousra Bouhanna](https://github.com/yousra-bouhanna)
- [Mohamed Riad Sahrane](https://github.com/riadshrn)
