# TDO4: Création des classes
# TD05: Mise à jour pour prendre en compte les classes filles de Document

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
        import re
        import pandas as pd 
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
        import re
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
        import pandas as pd
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
    

                                            
        
        