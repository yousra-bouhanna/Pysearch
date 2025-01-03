#1ère version: Socle de base de l'application, TD03 jusqu'au TD05
#--------!!!MISE JOUR POUR L'UTILISATION DE LA CLASSE DOCUMENT , LA CLASSE AUTHOR , LA CLASSE CORPUS et LES CLASSES FILLES!!!------
#Importations
import Document
import Author
import Corpus
import datetime
import praw
import urllib.request
import json
import xmltodict
import pandas as pd 
import DocumentFactory



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
hot_posts=reddit.subreddit('Chatgpt').hot(limit=300)
for i, post in enumerate(hot_posts):
    if post.selftext:  # On évite les posts sans texte
        date = datetime.datetime.fromtimestamp(post.created, tz=datetime.timezone.utc)#Ajouté avec l'aide de copilot pour la résolution d'une erreur de comparaison de dates
        num_comments = post.num_comments
        doc = DocumentFactory.DocumentFactory.create_document('Reddit', titre=post.title, auteur=post.author, date=date, url=post.url, texte=post.selftext, nb_com=post.num_comments)
        id2doc[i] = doc
        author_name = str(post.author)
        if author_name not in id2aut:
            id2aut[author_name] = Author.Author(author_name)
        id2aut[author_name].add(doc)

print(len(id2doc))
print(len(id2aut))

# Scraping des données ArXiV
query="Chatgpt"
url="http://export.arxiv.org/api/query?search_query=all:"+query+"&start=0&max_results=200"
data=urllib.request.urlopen(url).read()
data=data.decode()
# Conversion de data qui est sous forme XML en dictionnaire
dic=xmltodict.parse(data)
docs=dic["feed"]["entry"]
for i, doc in enumerate(docs):
    authors = doc["author"]
    author_names = [author["name"] for author in authors] if isinstance(authors, list) else [authors["name"]]
    date = datetime.datetime.fromisoformat(doc["published"].replace("Z", "+00:00"))
    doc = DocumentFactory.DocumentFactory.create_document('ArXiv', titre=doc["title"], auteur=author_names, date=date, url=doc["id"], texte=doc["summary"])
    for author_name in author_names:
        if author_name not in id2aut:
            id2aut[author_name] = Author.Author(author_name)
        id2aut[author_name].add(doc)
    
    id2doc[i + 200] = doc

print(len(id2doc))
print(len(id2aut))

#3.2: Sauvegarde des données
'''
Pour éviter d'intéroger les APIs à chaque fois, on va sauvegarder les données dans un dataframe
'''
# Mise à jour du dataframe pour prendre en compte les attributs de la classe Document
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

#Statistiques pour un auteur donnéc
print(id2aut[list(id2aut.keys())[123]].stats())

# 4.4: Création du corpus
corpus=Corpus.Corpus("Mon corpus", id2aut, id2doc)
print(corpus)

# Les filtres pour les documents
#print(corpus.sort_by_date(5, order="old"))
#print(corpus.sort_by_date(5, order="recent"))
print(corpus.sort_by_title(5, order="desc"))
#print(corpus.sort_by_title(5, order="asc"))

#4.5: Sauvegarde du corpus
corpus.save("corpus.pkl")

#4.6: Chargement du corpus
corpus=corpus.load("corpus.pkl")

