# TDO4: Création des classes
# TD05: Mise à jour pour prendre en compte les classes filles de Document

import numpy as np
from scipy.sparse import csr_matrix
import re
import pandas as pd

#4.3: Création de la classe Corpus
'''
La classe Corpus aura pour attributs:
- nom 
- authors : id2aut
- id2doc 
- ndoc : nombre des documents
- naut : nombre des auteurs
'''
import Author
import Document
import pickle

class Corpus:
    _instance = None
    # 5.4: Utilisation du patron de conception singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Corpus, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, nom, authors, id2doc, all_texts):
        self.nom = nom
        self.authors = authors
        self.id2doc = id2doc
        self.ndoc = len(id2doc)
        self.naut = len(authors)
        self.initialized = True
        self.all_texts=all_texts

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
    def load(self, filename):
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
            concordancier = concordancier.append({"Contexte gauche":cg, "Expression trouvée":self.all_texts[debut:fin], "Contexte droit":cd}, ignore_index=True)
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
        # je pense que c'est plus simple d'utiliser la chaine de caractères all_texts au lieu de parcourir tous les documents
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
            texte = self.clean_text(doc.texte)
            mots = texte.split()
            for mot in mots:
                if mot in vocabulaire:
                    vocabulaire[mot] += 1
        # on construit un dataframe avec une colonne pour les mots du vocabulaire et une colonne pour les occurences 
        freq = pd.DataFrame([(k, v) for k, v in vocabulaire.items()], columns=["Mot", "nbr_occurence"])
        return freq
    
    #6.6: Méthode pour mettre à jour la table freq avec le nombre de documents qui contiennent chaque mot
    def  nbr_documents(self):
        freq = self.nbr_occurence()
        for i, row in freq.iterrows():
            mot = row['Mot']
            ndoc_count = 0
            for doc in self.id2doc.values():
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