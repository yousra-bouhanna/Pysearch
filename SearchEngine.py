# TD07: Création de la classe SearchEngine
'''
La classe SearchEngine aura pour attributs:
'''
from corpus import Corpus
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

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
    
    # Méthode pour chercher les documents les plus similaires à une requête
    def search(self, query, top_n=5):
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