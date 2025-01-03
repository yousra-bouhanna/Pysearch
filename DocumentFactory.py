# 5.4: Utilisation du patron de conception singleton

from Document import RedditDocument, ArXivDocument
'''
La classe DocumentFactory est une classe singleton qui permet de créer des documents.
Elle contient une méthode statique create_document qui prend en paramètre le type de document et les attributs du document.
Elle retourne une instance de la classe correspondante.
'''

class DocumentFactory:
    @staticmethod
    def create_document(doc_type, **kwargs):
        if doc_type == 'Reddit':
            return RedditDocument(**kwargs)
        elif doc_type == 'ArXiv':
            return ArXivDocument(**kwargs)
        else:
            raise ValueError(f"Type de document inconnu: {doc_type}")