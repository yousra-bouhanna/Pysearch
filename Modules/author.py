# TDO4: Création des classes

#4.2: Création de la classe Author
'''
La classe Author aura pour attributs:
- name 
- ndoc : nombre de documents publiés
- production : un dictionnaire des documents 
'''

class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {} # un dictionnaire pour pouvoir indexer les documents par leur id (si jamais plus tard)

    # Méthode pour alimenter l'attribut production
    def add(self, production):
        self.ndoc += 1
        self.production[self.ndoc] = production

    # Méthode pour un affichage digeste
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    
    # Méthode pour afficher les statistiques 
    def stats(self):
        taille_totale = 0
        for i in self.production:
            texte = getattr(self.production[i], "texte", None)
            if texte:
                taille_totale += len(self.production[i].texte)
        return f"Nombre de documents produits : {self.ndoc}\nTaille moyenne des documents : {taille_totale/self.ndoc if self.ndoc > 0 else 0}"