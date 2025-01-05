#2ème version: moteur de recherche, TD03 jusqu'au TD07
#Importations
from Modules.document import Document, RedditDocument, ArXivDocument
from Modules.author import Author
from Modules.corpus import Corpus, compare, plot_wordcloud
import datetime
import praw
import urllib.request
import json
import xmltodict
import pandas as pd 
import Modules.documentFactory as DocumentFactory
from Modules.searchEngine import SearchEngine
import os



#3.1: Chargement des données
'''
Extraction des données à partir des deux sources: Reddit et ArXiv
Pour les données Reddit, on va utiliser l'API Praw
Pour les données ArXiv, on va utiliser l'API urllib
La thématique choisie est Chatgpt
Tous les documents seront dans un dictionnaire (index, document) nommé id2doc
'''
# Scraping des données Reddit
reddit = praw.Reddit(client_id='c1P8veYayu3RTOnAeMOREw', client_secret='pBIMxgjrBv3TC2cpkROBFVbbnzSObw', user_agent='Red WebScraping')
'''
On va récupérer le titre, l'auteur, le texte et l'url de chaque post
'''
id2doc={}
id2aut={}
hot_posts=reddit.subreddit('Chatgpt').hot(limit=30)
for i, post in enumerate(hot_posts):
    if post.selftext:  # On évite les posts sans texte
        date = datetime.datetime.fromtimestamp(post.created, tz=datetime.timezone.utc)#Ajouté avec l'aide de copilot pour la résolution d'une erreur de comparaison de dates
        num_comments = post.num_comments
        doc = RedditDocument( titre=post.title, auteur=post.author, date=date, url=post.url, texte=post.selftext, nb_com=post.num_comments)
        id2doc[i] = doc
        author_name = str(post.author)
        if author_name not in id2aut:
            id2aut[author_name] = Author(author_name)
        id2aut[author_name].add(doc)

nbr_RedditDocuments = len(id2doc)
nbr_AuteurReddit = len(id2aut)
print("Nombre de documents Reddit: ", nbr_RedditDocuments)
print("Nombre d'auteurs Reddit: ", nbr_AuteurReddit)


# Scraping des données ArXiV
query="Chatgpt"
url="http://export.arxiv.org/api/query?search_query=all:"+query+"&start=0&max_results=30"
data=urllib.request.urlopen(url).read()
data=data.decode()
# Conversion de data qui est sous forme XML en dictionnaire
dic=xmltodict.parse(data)
docs=dic["feed"]["entry"]
for i, doc in enumerate(docs):
    authors = doc["author"]
    author_names = [author["name"] for author in authors] if isinstance(authors, list) else [authors["name"]]
    date = datetime.datetime.fromisoformat(doc["published"].replace("Z", "+00:00"))
    doc = ArXivDocument( titre=doc["title"], auteur=author_names, date=date, url=doc["id"], texte=doc["summary"])
    for author_name in author_names:
        if author_name not in id2aut:
            id2aut[author_name] = Author(author_name)
        id2aut[author_name].add(doc)
    
    id2doc[i + 200] = doc

nbr_ArXivDocuments = len(id2doc) - nbr_RedditDocuments
nbr_AuteurArXiv = len(id2aut) - nbr_AuteurReddit
print("Nombre de documents ArXiv: ", nbr_ArXivDocuments)
print("Nombre d'auteurs ArXiv: ", nbr_AuteurArXiv)


#3.2: Sauvegarde des données
'''
Pour éviter d'intéroger les APIs à chaque fois, on va sauvegarder les données dans un dataframe
'''
# Mise à jour du dataframe pour prendre en compte les attributs de la classe Document
data=pd.DataFrame(columns=["id", "titre","auteur","date","url","texte","origin"])
for i, doc in id2doc.items():
    data.loc[i]=[i, doc.titre, doc.auteur, doc.date, doc.url, doc.texte, doc.type]

# Create the directory if it doesn't exist
os.makedirs("Data", exist_ok=True)

# Sauvegarde du dataframe 
data.to_csv(os.path.join("Data", "data.csv"), sep="\t", index=False)

# Chargement en mémoire 
data = pd.read_csv(os.path.join("Data", "data.csv"), sep="\t")

#3.3: Manipulation des données 
'''
Quelques manipulations sur le corpus
'''

print("La taille du corpus est de: ", data.shape[0])   

# Nombre de mots et de phrases dans chaque document
for i, doc in enumerate(data["texte"]):
    print(f"Document n° {i}")
    print("Nombre de phrases: ", len(doc.split('.')))
    print("Nombre de mots: ", len(doc.split()))


# Suppression des documents trop petits 
data=data[data["texte"].apply(lambda x: len(x)>20)]
print("La taille du corpus aprés la suppression est de: ", data.shape[0])

# Mise à jour du fichier csv
data.to_csv(os.path.join("Data", "data.csv"), sep="\t", index=False)

# Chaine de caractères de tous les documents concaténés
all_texts=" ".join(data["texte"])
print("La longueur de la chaine de caractères est de: ", len(all_texts))

#Statistiques pour un auteur donnéc
print(id2aut[list(id2aut.keys())[1]].stats())

# 4.4: Création du corpus
corpus=Corpus("Mon corpus", id2aut, id2doc, all_texts)
print(corpus)

# Les filtres pour les documents
#print(corpus.sort_by_date(5, order="old"))
#print(corpus.sort_by_date(5, order="recent"))
print(corpus.sort_by_title(2, order="desc"))
#print(corpus.sort_by_title(5, order="asc"))

#4.5: Sauvegarde du corpus
corpus.save(os.path.join("Data", "corpus.pkl"))

#4.6: Chargement du corpus
corpus = Corpus.load(os.path.join("Data", "corpus.pkl"))
'''
#6.6: Affichage de la table freq
print(corpus.nbr_documents())

#7.2: Matrice termes-documents
print(corpus.build_mat_TF())

#7.3: Affichage des statistiques pour chaque mot
print(corpus.stats())

#7.4: Matrice TF-IDF
print(corpus.build_mat_TF_IDF())
'''
#7.5: Initialisation du moteur de recherche
moteur=SearchEngine(corpus)

#7.6: Recherche
requete=input("Entrez votre requête: ")

#7.7: Affichage des résultats
print(moteur.search(requete, top_n=3))

