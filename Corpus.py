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
    def __init__(self, nom, authors, id2doc):
        self.nom = nom
        self.authors = authors
        self.id2doc = id2doc
        self.ndoc = len(id2doc)
        self.naut = len(authors)

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
        
        