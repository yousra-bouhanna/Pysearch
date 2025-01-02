#1ère version: Scole de base de l'application, TD03 jusqu'au TD05
#--------!!!MISE JOUR POUR L'UTILISATION DE LA CLASSE DOCUMENT!!!------
#Importations
import Document
import datetime
import praw
import urllib.request
import json
import xmltodict


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
hot_posts=reddit.subreddit('Chatgpt').hot(limit=300)
for i, post in enumerate(hot_posts):
    if post.selftext:  # Vérifie si le texte n'est pas vide
        doc = Document.Document(titre=post.title, auteur=post.author, date=datetime.datetime.fromtimestamp(post.created), url=post.url, texte=post.selftext)
        id2doc[i] = doc
        print(f"Reddit Post {i}: {doc.titre}, {doc.auteur}, {doc.date}, {doc.url}, {len(doc.texte)} characters")
print(len(id2doc))

# Scraping des données ArXiV
query="Chatgpt"
url="http://export.arxiv.org/api/query?search_query=all:"+query+"&start=0&max_results=200"
data=urllib.request.urlopen(url).read()
data=data.decode()
# Conversion de data qui est sous forme XML en dictionnaire
dic=xmltodict.parse(data)
docs=dic["feed"]["entry"]
for i, doc in enumerate(docs):
    doc=Document.Document(titre=doc["title"], auteur=doc["author"], date=doc["published"], url=doc["id"], texte=doc["summary"])
    id2doc[i+200]=doc

print(len(id2doc))

#3.2: Sauvegarde des données
'''
Pour éviter d'intéroger les APIs à chaque fois, on va sauvegarder les données dans un dataframe
'''
# Mise à jour du dataframe pour prendre en compte les attributs de la classe Document
import pandas as pd 
data=pd.DataFrame(columns=["id", "titre","auteur","date","url","texte","origin"])
for i, doc in id2doc.items():
    if i<200:
        data.loc[i]=[i, doc.titre, doc.auteur, doc.date, doc.url, doc.texte, "Reddit"]
    else:
        data.loc[i]=[i, doc.titre, doc.auteur, doc.date, doc.url, doc.texte, "ArXiv"]
print(data.head())
# Sauvgarde du dataframe
data.to_csv("data.csv", sep="\t", index=False)
# Chargement en mémoire
data=pd.read_csv("data.csv", sep="\t")

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
data.to_csv("data.csv", sep="\t", index=False)

# Chaine de caractères de tous les documents concaténés
all_docs=" ".join(data["texte"])
print(len(all_docs))
