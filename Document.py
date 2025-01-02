# TDO4: Création des classes

#4.1: Création de la classe Document
'''
La classe Document aura pour attributs:
- titre
- auteur
- date
- url
- texte 

'''
class Document:
    def __init__(self, titre='', auteur='', date='', url='', texte=''):
        self.titre=titre
        self.auteur=auteur
        self.date=date
        self.url=url
        self.texte=texte

    # Méthode pour un affichage complet
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"
    # Fonction pour un affichage digeste
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    
    
