import unittest
import sys
import os
from Modules.corpus import Corpus, compare

class TestCorpus(unittest.TestCase):

    def setUp(self):
        # Chargement des corpus réels
        self.corpus1 = Corpus.load(os.path.join("Data", "corpus.pkl"))
        self.corpus2 = Corpus.load(os.path.join("Data", "discours.pkl"))

    def test_compare_inputs(self):
        # Vérifier que les entrées de la fonction compare sont bien des instances de Corpus
        self.assertIsInstance(self.corpus1, Corpus)
        self.assertIsInstance(self.corpus2, Corpus)

    def test_compare_output(self):
        # Vérifier que la sortie de la fonction compare est correcte
        common_words, specific_words1, specific_words2 = compare(self.corpus1, self.corpus2)
        self.assertIsInstance(common_words, list)
        self.assertIsInstance(specific_words1, list)
        self.assertIsInstance(specific_words2, list)

    def test_compare_non_empty(self):
        # Vérifier que les résultats de la comparaison ne sont pas vides
        common_words, specific_words1, specific_words2 = compare(self.corpus1, self.corpus2)
        self.assertGreater(len(common_words), 0)
        self.assertGreater(len(specific_words1), 0)
        self.assertGreater(len(specific_words2), 0)

    def test_compare_invalid_inputs(self):
        # Vérifier que la fonction compare lève une exception pour des entrées invalides
        with self.assertRaises(TypeError):
            compare("not a corpus", self.corpus2)
        with self.assertRaises(TypeError):
            compare(self.corpus1, "not a corpus")

if __name__ == '__main__':
    unittest.main()