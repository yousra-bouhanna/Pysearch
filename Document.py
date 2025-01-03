# TDO4: Création des classes
# TD05: Héritage

#4.1: Création de la classe Document
'''
La classe Document aura pour attributs:
- titre
- auteur
- date
- url
- texte 

'''
'''Vous devez pouvoir afficher la liste des articles contenus dans votre Corpus avec la source (Reddit
 ou Arxiv) d'où ils proviennent. Pour cela, il existe plusieurs solutions, mais vous implémenterez celle qui
 consiste à ajouter un champ type à la classe mère Document et à implémenter la méthode getType()
 directement dans les classes filles, comme vu en cours.'''

class Document:
    # 5.3: Ajout de l'attribut type
    def __init__(self, titre='', auteur='', date='', url='', texte='', type=''):
        self.titre=titre
        self.auteur=auteur
        self.date=date
        self.url=url
        self.texte=texte
        self.type=type

    # Méthode pour un affichage complet
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"
    # Méthode pour un affichage digeste
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    

# 5.1: Création de la classe fille RedditDocument
'''
La classe RedditDocument est une classe fille de la classe Document. 
Elle hérite de tous les attributs de la classe Document et en ajoute un nouveau: le nombre de commentaires.
'''
class RedditDocument(Document):
    def __init__(self, titre='', auteur='', date='', url='', texte='', nb_com=0):
        # Appel du constructeur de la classe mère en utilisant super
        super().__init__(titre, auteur, date, url, texte, type='Reddit')
        self.nb_com=nb_com

    # Méthode pour un affichage complet
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\tNombre de commentaires : {self.nb_com}"
    
    # Méthode pour un affichage digeste
    def __str__(self):
        return f"{self.titre}, par {self.auteur}, {self.nb_com} commentaires"
    
    # Méthode getteur pour le nombre de commentaires
    def get_nb_com(self):
        return self.nb_com
    
    # Méthode setteur pour le nombre de commentaires
    def set_nb_com(self, nb_com):
        self.nb_com=nb_com
    
    # Méthode pour obtenir le type
    def getType(self):
        return self.type

# 5.2: Création de la classe fille ArXivDocument
'''
La classe ArXivDocument est une classe fille de la classe Document.
Elle hérite de tous les attributs,mais l'attribut auteur devient une liste d'auteurs.
'''
class ArXivDocument(Document):
    def __init__(self, titre='', auteur=[], date='', url='', texte=''):
        # Appel du constructeur de la classe mère en utilisant super
        super().__init__(titre, auteur, date, url, texte, type='ArXiv')
    
    # Méthode pour un affichage complet
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"
    
    # Méthode pour un affichage digeste
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    
    # Méthode getteur pour le nombre d'auteurs
    def get_auteur(self):
        return len(self.auteur)
    
    # Méthode pour obtenir le type
    def getType(self):
        return self.type
    
    