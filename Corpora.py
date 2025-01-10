#==========================Préparation des corpus pour le moteur de recherche====================================
# On va créer un corpus pour chaque type de document (Reddit et Arxiv) et un corpus global.
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

# Scapping des données Reddit 
reddit = praw.Reddit(client_id='c1P8veYayu3RTOnAeMOREw', client_secret='pBIMxgjrBv3TC2cpkROBFVbbnzSObw', user_agent='Red WebScraping')
id2doc = {}
id2aut = {}
reddit_id2doc = {}
reddit_id2aut = {}
hot_posts = reddit.subreddit('NLP').hot(limit=20000)
for i, post in enumerate(hot_posts):
    if post.selftext:  # On évite les posts sans texte
        date = datetime.datetime.fromtimestamp(post.created, tz=datetime.timezone.utc)  # Ajouté avec l'aide de copilot pour la résolution d'une erreur de comparaison de dates
        num_comments = post.num_comments
        doc = RedditDocument(titre=post.title, auteur=post.author, date=date, url=post.url, texte=post.selftext, nb_com=post.num_comments)
        id2doc[i] = doc
        reddit_id2doc[i] = doc
        author_name = str(post.author)
        if author_name not in id2aut:
            id2aut[author_name] = Author(author_name)
        if author_name not in reddit_id2aut:
            reddit_id2aut[author_name] = Author(author_name)
        id2aut[author_name].add(doc)
        reddit_id2aut[author_name].add(doc)

# Sauvgarde des documents Reddit sous format csv 
Reddit_data = pd.DataFrame(columns=["id", "titre", "auteur", "date", "url", "texte", "origin"])
for i, doc in reddit_id2doc.items():
    Reddit_data.loc[i] = [i, doc.titre, doc.auteur, doc.date, doc.url, doc.texte, doc.type]
Reddit_data.to_csv(os.path.join("Data", "Reddit_data.csv"), sep="\t", index=False)

# La chaîne de caractère qui contient le texte de tous les documents Reddit
texte_reddit = " ".join([doc.texte for doc in reddit_id2doc.values()])

# Création du corpus Reddit
corpus_reddit = Corpus("Reddit_corpus", reddit_id2aut, reddit_id2doc, texte_reddit)
corpus_reddit.save(os.path.join("Data", "Reddit_corpus.pkl"))
print(corpus_reddit)

# Scraping des données ArXiv
query = "NLP"
url = "http://export.arxiv.org/api/query?search_query=all:" + query + "&start=0&max_results=1000"
data = urllib.request.urlopen(url).read()
data = data.decode()
# Conversion de data qui est sous forme XML en dictionnaire
dic = xmltodict.parse(data)
docs = dic["feed"]["entry"]
arxiv_id2doc = {}
arxiv_id2aut = {}
for i, doc in enumerate(docs):
    authors = doc["author"]
    author_names = [author["name"] for author in authors] if isinstance(authors, list) else [authors["name"]]
    date = datetime.datetime.fromisoformat(doc["published"].replace("Z", "+00:00"))
    doc = ArXivDocument(titre=doc["title"], auteur=author_names, date=date, url=doc["id"], texte=doc["summary"])
    for author_name in author_names:
        if author_name not in id2aut:
            id2aut[author_name] = Author(author_name)
        if author_name not in arxiv_id2aut:
            arxiv_id2aut[author_name] = Author(author_name)
        id2aut[author_name].add(doc)
        arxiv_id2aut[author_name].add(doc)
    
    arxiv_id2doc[max(arxiv_id2doc.keys(), default=0) + 1] = doc
    id2doc[max(id2doc.keys(), default=0) + 1] = doc

# Sauvgarde des documents ArXiv sous format csv
Arxiv_data = pd.DataFrame(columns=["id", "titre", "auteur", "date", "url", "texte", "origin"])
for i, doc in arxiv_id2doc.items():
    Arxiv_data.loc[i] = [i, doc.titre, doc.auteur, doc.date, doc.url, doc.texte, doc.type]
Arxiv_data.to_csv(os.path.join("Data", "Arxiv_data.csv"), sep="\t", index=False)

# La chaîne de caractère qui contient le texte de tous les documents ArXiv
texte_arxiv = " ".join([doc.texte for doc in arxiv_id2doc.values()])

# Création du corpus ArXiv
corpus_arxiv = Corpus("ArXiv_corpus", arxiv_id2aut, arxiv_id2doc, texte_arxiv)
corpus_arxiv.save(os.path.join("Data", "ArXiv_corpus.pkl"))
print(corpus_arxiv)

# Création du corpus global
texte_global = texte_reddit + " " + texte_arxiv
corpus_global = Corpus("Global_corpus", id2aut, id2doc, texte_global)
corpus_global.save(os.path.join("Data", "Global_corpus.pkl"))
print(corpus_global)
