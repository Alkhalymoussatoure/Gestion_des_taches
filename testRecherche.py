import unittest
import os
from io import StringIO
import sys
from fonctions import Rechercher_tache,chemin_fichier

# Création d'un fichier de test temporaire
test_chemin_fichier = chemin_fichier 

class TestRechercherTache(unittest.TestCase):

    def setUp(self):
        """ Prépare le fichier de test. """
        global chemin_fichier
        chemin_fichier = test_chemin_fichier  # Utiliser un fichier temporaire

        with open(chemin_fichier, 'w', encoding="utf-8") as f:
            f.write("Tâche 1;Description de la tâche 1;moyenne;en cours;2025-12-31\n")
            f.write("Tâche 2;Autre description;moyenne;à faire;2025-12-31\n")

    def tearDown(self):
        """ Supprime le fichier après chaque test. """
        if os.path.exists(chemin_fichier):
            os.remove(chemin_fichier)

    def test_recherche_tache_existante(self):
        """ Vérifie que la recherche trouve une tâche existante. """
        sys.stdin = StringIO("Tâche 1\n")  # Simuler l'entrée utilisateur
        sys.stdout = output = StringIO()  # Capturer la sortie de la fonction

        Rechercher_tache()  # Appel de la fonction sans paramètre

        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        self.assertIn("Tâche No:1", output.getvalue(), "La tâche recherchée doit être trouvée.")

    def test_recherche_tache_inexistante(self):
        """ Vérifie que la recherche ne trouve pas une tâche inexistante. """
        sys.stdin = StringIO("Tâche 3\n")  # Simuler l'entrée utilisateur
        sys.stdout = output = StringIO()  # Capturer la sortie

        Rechercher_tache()  # Appel de la fonction sans paramètre

        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        self.assertIn("Aucune tâche trouvée.", output.getvalue(), "La recherche ne doit rien trouver.")

if __name__ == "__main__":
    unittest.main()
