# TDO4: Création des classes
# TD05: Mise à jour pour prendre en compte les classes filles de Document

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import os
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

#4.3: Création de la classe Corpus
'''
La classe Corpus aura pour attributs:
- nom 
- authors : id2aut
- id2doc 
- ndoc : nombre des documents
- naut : nombre des auteurs
'''
from Modules.author import Author
from Modules.document import Document
import pickle

class Corpus:
    '''
    _instance = None
    # 5.4: Utilisation du patron de conception singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Corpus, cls).__new__(cls)
        return cls._instance
    '''
    def __init__(self, nom, authors=None, id2doc=None, all_texts=""):
        self.nom = nom
        self.authors = authors if authors is not None else {}
        self.id2doc = id2doc if id2doc is not None else {}
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)
        #self.initialized = True
        self.all_texts = all_texts

    # Méthode pour ajouter un document
    def add(self, doc):
        if isinstance(doc.auteur, list):
            for auteur in doc.auteur:
                if auteur not in self.authors:
                    self.naut += 1
                    self.authors[auteur] = Author(auteur)
                self.authors[auteur].add(doc.texte)
        else:
            if doc.auteur not in self.authors:
                self.naut += 1
                self.authors[doc.auteur] = Author(doc.auteur)
            self.authors[doc.auteur].add(doc.texte)
        
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        self.all_texts += " " + doc.texte
    
    # Méthode pour un affichage digeste
    def __str__(self):
        return f"Nom du corpus : {self.nom}\nNombre d'auteurs : {self.naut}\nNombre de documents : {self.ndoc}"
    
    # Méthode pour afficher les documents selon l'ordre de publication
    def sort_by_date(self, n, order='recent'):
        reverse = True if order == 'recent' else False
        return sorted(self.id2doc.values(), key=lambda x: x.date, reverse=reverse)[:n]
    
    # Méthode pour afficher les documents selon l'ordre alphabétique des titres
    def sort_by_title(self, n, order='asc'):
        reverse = True if order == 'desc' else False
        return sorted(self.id2doc.values(), key=lambda x: x.titre.lower(), reverse=reverse)[:n]
    
    # Méthode pour sauvegarder le corpus en utilisant pickle
    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    # Méthode pour charger le corpus en utilisant pickle
    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
        
    #6.1: Méthode pour savoir si un mot est dans le corpus
    def search(self, mot):
        if mot in self.all_texts:
            return True
        else:
            return False
        
    #6.2: Méthode qui permet de créer un concordancier pour une expression 
    def concorde(self, expression, contexte): # contexte ici est la taille du contexte 
        # on utilise la fonction finditer pour trouver toutes les occurences de l'expression dans la chaine de caractères
        resultats = re.finditer(expression, self.all_texts)
        concordancier=pd.DataFrame(columns=["Contexte gauche", "Expression trouvée", "Contexte droit"])
        for resultat in resultats:
            debut, fin = resultat.start(), resultat.end()
            cg = self.all_texts[debut-contexte:debut]
            cd = self.all_texts[fin:fin+contexte]
            concordancier = pd.concat([concordancier, pd.DataFrame([{"Contexte gauche": cg, "Expression trouvée": self.all_texts[debut:fin], "Contexte droit": cd}])], ignore_index=True)
        return concordancier
    
    #6.3: Méthode pour nettoyer un texte
    def clean_text(self, texte):
        texte = re.sub(r"\n", " ", texte)
        texte = re.sub(r"[.,;:!?]", " ", texte)
        texte = re.sub(r"[0-9]", " ", texte)
        texte = re.sub(r"[^a-z ]", " ", texte.lower())
        texte = re.sub(r"\s+", " ", texte).strip()
        return texte
    
    #6.4: Méthode pour créer le vocabulaire du corpus
    def vocabulary(self):
        # c'est plus simple d'utiliser la chaine de caractères all_texts au lieu de parcourir tous les documents
        all_texts=self.clean_text(self.all_texts)
        # on utilise set pour éliminer les doublons
        mots=set(all_texts.split())
        vocabulaire={}
        for mot in mots:
            vocabulaire[mot]=0 # on initialise le nombre d'occurences à 0
        return vocabulaire
    
    #6.5: Méthode pour calculer le nombre d'occurence de chaque mot du vocabulaire dans le corpus
    def nbr_occurence(self):
        vocabulaire = self.vocabulary()
        for doc in self.id2doc.values():
            if hasattr(doc, 'texte') and isinstance(doc.texte, str):
                texte = self.clean_text(doc.texte)
                mots = texte.split()
                for mot in mots:
                    if mot in vocabulaire:
                        vocabulaire[mot] += 1
        # on construit un dataframe avec une colonne pour les mots du vocabulaire et une colonne pour les occurences 
        freq = pd.DataFrame([(k, v) for k, v in vocabulaire.items()], columns=["Mot", "nbr_occurence"])
        return freq
    
    #6.6: Méthode pour mettre à jour la table freq avec le nombre de documents qui contiennent chaque mot
    def nbr_documents(self):
        freq = self.nbr_occurence()

        # Limiter aux 100 premiers mots les plus fréquents
        freq = freq.sort_values(by="nbr_occurence", ascending=False).head(50)      

        for i, row in freq.iterrows():
            mot = row['Mot']
            ndoc_count = 0

            for doc in self.id2doc.values():
                if hasattr(doc, 'texte') and isinstance(doc.texte, str):
                    texte = self.clean_text(doc.texte)
                    if mot in texte:
                        ndoc_count += 1

            freq.loc[i, 'nbr_documents'] = ndoc_count

        return freq

    
    #7.1: Méthode pour mettre à jour le dictionnaire vocabulaire, les mots seront triés par ordre alphabétique et chaque mot va indexer un autre dictionnaire contenant un id unique et le nombre d'occurence du mot en question
    def vocab(self):
        vocab = self.vocabulary()
        vocab = {k:{"id":i, "nbr_occurence":v} for i, (k, v) in enumerate(sorted(vocab.items()))}
        return vocab

    #7.2: Méthode pour construite la matrice document-terme
    def build_mat_TF(self):
        vocab = self.vocab()
        nombre_mots=len(vocab)        
        nombre_documents=len(self.id2doc)
        # j'ai utilisé copilot pour cette méthode
        # Initialisation des listes pour construite la matrice creuse
        data = [] #nombre d'occurence de chaque mot dans chaque document
        lignes = [] #indices des documents
        colonnes = [] #indices des mots
        doc_index_mapping = {doc_id: idx for idx, doc_id in enumerate(self.id2doc.keys())} #pour assurer la bonne correspondance entre les indices des documents et les indices des lignes de la matrice creuse
        for doc_id, doc in self.id2doc.items():
            texte = self.clean_text(doc.texte)
            mots = texte.split()
            mot_occ={} #dictionnaire pour stocker le nombre d'occurence de chaque mot dans le document
            for mot in mots:
                if mot in vocab:
                    mot_id = vocab[mot]["id"]
                    if mot_id not in mot_occ:
                        mot_occ[mot_id] = 0
                    mot_occ[mot_id] += 1

            for mot_id, count in mot_occ.items():
                    lignes.append(doc_index_mapping[doc_id])
                    colonnes.append(mot_id)
                    data.append(count)

        # Construction de la matrice creuse
        mat_TF=csr_matrix((data, (lignes, colonnes)), shape=(nombre_documents, nombre_mots))
        self.doc_index_mapping = doc_index_mapping

        return mat_TF
    
    #7.3: Méthode pour calculer des statistiques pour chaque mot du vocabulaire
    def stats(self):
        mat_TF = self.build_mat_TF()
        vocab = self.vocab()
        for mot in vocab:
            mot_id = vocab[mot]["id"]
            vocab[mot]["total_occurences"] = mat_TF[:,mot_id].sum() # somme des occurences de chaque mot dans tout le corpus
            vocab[mot]["total_documents"] = (mat_TF[:,mot_id]>0).sum() # somme des documents qui contiennent chaque mot
        # on supprime 'nbr_occurence' du dictionnaire vocab
        for mot in vocab:
            del vocab[mot]["nbr_occurence"] 
        return vocab
        
    # 7.4: Méthode pour construire la matrice TF-IDF 
    def build_mat_TF_IDF(self):
        mat_TF = self.build_mat_TF()
        vocab = self.vocab()
        nombre_documents, nombre_mots = mat_TF.shape
        # Initialisation de la matrice creuse
        data = []
        lignes = []
        colonnes = []
        for mot in vocab:
            mot_id = vocab[mot]["id"]
            # Calcul de l'IDF
            vocab[mot]["IDF"] = np.log(nombre_documents / (1 + (mat_TF[:,mot_id]>0).sum()))
            # Calcul de la matrice TF-IDF
            for doc_id, doc in enumerate(self.id2doc.values()):
                data.append(mat_TF[doc_id, mot_id] * vocab[mot]["IDF"])
                lignes.append(doc_id)
                colonnes.append(mot_id)
        mat_TF_IDF = csr_matrix((data, (lignes, colonnes)), shape=(nombre_documents, nombre_mots))
        return mat_TF_IDF
    
    #9.2: Méthode pour afficher l'évolution temporelle d'un mot ou d'un groupe de mots dans le corpus 
    def evolution_temporelle(self, mots, freq='M'):
        '''
        :param mots: Liste de mots à observer
        :param freq: Fréquence de découpage ('Y' pour année, 'M' pour mois)
        :return: DataFrame avec les occurrences des mots par période et le plot
        
        '''
        # Initialisation du dictionnaire pour stocker les occurrences des mots
        # dictionnaire de dictionnaires 
        occurrences = defaultdict(lambda: defaultdict(int))
        
        # Parcours des documents pour compter les occurrences des mots par période
        for doc in self.id2doc.values():
            date = pd.to_datetime(doc.date)
            #Découpage temporel
            periode = date.to_period(freq)
            for mot in mots:
                occurrences[periode][mot] += doc.texte.lower().split().count(mot.lower())
        
        # Conversion du dictionnaire en DataFrame
        df = pd.DataFrame(occurrences).T.fillna(0)

        # Tracer le graphique
        ax = df.plot(kind='line', figsize=(10, 5))
        plt.title("Évolution temporelle des mots")
        plt.xlabel("Période")
        plt.ylabel("Occurrences")
        plt.legend(mots)
        plt.show()
        
        return df, ax

   
# Fonction pour comparer deux corpus
def compare(corpus1, corpus2, top_n=100):
    if not isinstance(corpus1, Corpus) or not isinstance(corpus2, Corpus):
        raise TypeError("Les entrées doivent être des instances de la classe Corpus.")
    
    texte1 = corpus1.all_texts
    texte2 = corpus2.all_texts

    # Vectorisation TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([texte1, texte2])

    # Extraction des mots et des scores 
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = X.toarray()

    # Séparation des scores
    scores1 = tfidf_scores[0]
    scores2 = tfidf_scores[1]

    #Identification des mots communs et mots spécifiques
    common_words = set(feature_names[scores1 > 0]) & set(feature_names[scores2 > 0])
    specific_words1 = set(feature_names[scores1 > 0]) - common_words
    specific_words2 = set(feature_names[scores2 > 0]) - common_words
    
    # Limiter le nombre de mots affichés (fait avec l'aide de copilot)
    common_words = sorted(common_words, key=lambda x: scores1[feature_names.tolist().index(x)] + scores2[feature_names.tolist().index(x)], reverse=True)[:top_n]
    specific_words1 = sorted(specific_words1, key=lambda x: scores1[feature_names.tolist().index(x)], reverse=True)[:top_n]
    specific_words2 = sorted(specific_words2, key=lambda x: scores2[feature_names.tolist().index(x)], reverse=True)[:top_n]

    return common_words, specific_words1, specific_words2

'''
# Une manière plus simple de comparer les corpus en utilisant ce qui a été fait dans la classe Corpus
def compare(corpus1, corpus2):

    # Obtenir le vocabulaire des deux corpus
    vocab1 = corpus1.vocab()
    vocab2 = corpus2.vocab()
    
    # Obtenir les mots du vocabulaire
    words1 = set(vocab1.keys())
    words2 = set(vocab2.keys())
    
    # Identification des mots communs et spécifiques
    common_words = words1 & words2
    specific_words1 = words1 - common_words
    specific_words2 = words2 - common_words
    
    return common_words, specific_words1, specific_words2
'''

# Fonction pour afficher un nuage de mots (utilisée pour la comparaison des corpus)
# Créer le répertoire de sortie s'il n'existe pas
def plot_wordcloud(words, title, Outputs="Outputs"):

    if not os.path.exists(Outputs):
        os.makedirs(Outputs)
        
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')
    # Enregistrer la figure en tant que fichier PNG
    output_path = os.path.join(Outputs, f"{title}.png")
    plt.savefig(output_path, format='png')
    plt.show()
    plt.close()

    