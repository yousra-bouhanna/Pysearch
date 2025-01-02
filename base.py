#1ère version: Scole de base de l'application, TD03 jusqu'au TD05

#3.1: Chargement des données
'''
Extraction des données à partir des deux sources: Reddit et ArXiv
Pour les données Reddit, on va utiliser l'API Praw
Pour les données ArXiv, on va utiliser l'API urllib
La thématique choisie est Chatgpt
Tous les documents seront dans une liste docs pour l'instant
'''
docs=[]
# Scraping des données Reddit
import praw
reddit = praw.Reddit(client_id='c1P8veYayu3RTOnAeMOREw', client_secret='pBIMxgjrBv3TC2cpkROBFVbbnzSObw', user_agent='Red WebScraping')
'''
Dans un premier temps on va récupérer que le titre et le selftext des posts, cependant on peut récupérer d'autres informations comme le score, le nombre de commentaires, l'auteur, l'heure de publication, etc.
'''
hot_posts=reddit.subreddit('Chatgpt').hot(limit=200)
# Concaténation du titre et du selftext
for post in hot_posts:
    doc=post.title + " " + post.selftext
    doc=doc.replace("\n", " ")
    docs.append(doc)

# Scraping des données ArXiv
import urllib.request
import json
import xmltodict

query="Chatgpt"
url="http://export.arxiv.org/api/query?search_query=all:"+query+"&start=0&max_results=200"
data=urllib.request.urlopen(url).read()
data=data.decode()
# Conversion de data qui est sous forme XML en dictionnaire
dic=xmltodict.parse(data)
arxiv_docs=dic['feed']['entry']
for entry in arxiv_docs:
    doc=entry['title'] + " " + entry['summary']
    doc=doc.replace("\n", " ")
    docs.append(doc)

#3.2: Sauvegarde des données
'''
Pour éviter d'intéroger les APIs à chaque fois, on va sauvegarder les données dans un dataframe
'''
import pandas as pd 
data=pd.DataFrame(columns=["id", "text", "origin"])
rows = [{"id": i, "text": doc, "origin": "Reddit" if i < 200 else "ArXiv"} for i, doc in enumerate(docs)]
data = pd.concat([data, pd.DataFrame(rows)], ignore_index=True)
print(data.shape)
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
for doc in data["text"]:
    print("Document n°", data[data["text"]==doc].index[0])
    print("Nombre de phrases: ", len(doc.split(".")))
    print("Nombre de mots: ", len(doc.split(" ")))

# Suppression des documents trop petits 
data=data[data["text"].apply(lambda x: len(x)>20)]
print("La taille du corpus aprés la suppression est de: ", data.shape[0])

# Mise à jour du fichier csv
data.to_csv("data.csv", sep="\t", index=False)

# Chaine de caractères de tous les documents concaténés
all_docs=" ".join(data["text"])
print(len(all_docs))
