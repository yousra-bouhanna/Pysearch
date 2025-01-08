# TD07: Création de la classe SearchEngine
'''
La classe SearchEngine aura pour attributs:
'''
from Modules.corpus import Corpus
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer

class SearchEngine:
    def __init__(self, corpus):
        self.corpus=corpus
        self.mat_TF = self.corpus.build_mat_TF()
        self.doc_index_mapping = self.corpus.doc_index_mapping
        self.vocab = self.corpus.vocab()
        self.id2doc = self.corpus.id2doc
    
    # Méthode pour transofrmer une requête (les mots clés) en vecteur
    def transform_query(self, query):
        query=query.lower()
        query_words = query.split()
        query_vector = np.zeros(len(self.vocab))
        for word in query_words:
            if word in self.vocab:
                word_id = self.vocab[word]["id"]
                query_vector[word_id] += 1
        return query_vector
    
    # Méthode pour chercher les documents les plus similaires à une requête en utilisant la matrice TF 
    def search_tf(self, query, top_n=5):
        query_vector = self.transform_query(query)
        query_vector = query_vector.reshape(1, -1)
        similarities = cosine_similarity(query_vector, self.mat_TF).flatten()
        top_indices = similarities.argsort()[-top_n:][::-1]
        results = []
        for idx in tqdm(top_indices, desc="Recherche des documents"):
            doc_id=list(self.doc_index_mapping.keys())[list(self.doc_index_mapping.values()).index(idx)]
            doc = self.id2doc[doc_id]
            results.append({
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "similarité": similarities[idx]
            })
        return pd.DataFrame(results)
    
    # Méthode pour chercher les documents les plus similaires à une requête en utilisant la matrice TF-IDF
    def search_tfidf(self, query, top_n=5):
        documents = [doc.texte for doc in self.id2doc.values()]
        vectorizer = TfidfVectorizer()
        mat_TFIDF = vectorizer.fit_transform(documents)
        query_vector = vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, mat_TFIDF).flatten()
        top_indices = similarities.argsort()[-top_n:][::-1]
        results = []
        for idx in tqdm(top_indices, desc="Recherche des documents"):
            doc_id = list(self.doc_index_mapping.keys())[list(self.doc_index_mapping.values()).index(idx)]
            doc = self.id2doc[doc_id]
            results.append({
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "similarité": similarities[idx]
            })
        return pd.DataFrame(results)
    
    # Méthode pour faire une recherche sur l'auteur 
    def search_author(self, author, top_n=5):
        author = author.lower()
        results = []
        for doc_id, doc in self.id2doc.items():
            if doc.auteur.lower() == author:
                results.append({
                    "titre": doc.titre,
                    "auteur": doc.auteur,
                    "date": doc.date,
                    "url": doc.url
                })
        return pd.DataFrame(results)
    
    # Méthode pour faire une recherche sur la date
    def search_date(self, date, top_n=5):
        results = []
        for doc_id, doc in self.id2doc.items():
            if doc.date == date:
                results.append({
                    "titre": doc.titre,
                    "auteur": doc.auteur,
                    "date": doc.date,
                    "url": doc.url
                })
        return pd.DataFrame(results)
    
    # Méthode pour faire une recherche sur la source du document (Reddit ou Arxiv)
    def search_source(self, source, top_n=5):
        results = []
        for doc_id, doc in self.id2doc.items():
            if doc.type == source:
                results.append({
                    "titre": doc.titre,
                    "auteur": doc.auteur,
                    "date": doc.date,
                    "url": doc.url
                })
        return pd.DataFrame(results)
    


    

