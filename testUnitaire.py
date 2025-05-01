import unittest
import os
from fonctions import *

# Fichiers temporaires pour les tests
test_chemin_fichier = "test_taches.txt"
test_chemin_journal = "test_journal.csv"

class TestGestionTaches(unittest.TestCase):

    def setUp(self):
        """ Création de fichiers de test avant chaque test. """
        with open(test_chemin_fichier, 'w', encoding="utf-8") as f:
            f.write("Test Tâche;Description test;moyenne;en cours;2025-12-31\n")
        with open(test_chemin_journal, 'w', encoding="utf-8") as f:
            f.write("Date de modification;Action;Informations sur la tâche\n")

   

    def test_Liste_des_taches(self):
        """ Vérifie que la liste des tâches est bien affichée. """
        with open(test_chemin_fichier, 'r', encoding="utf-8") as f:
            contenu = f.readlines()
        self.assertTrue(len(contenu) > 0, "Le fichier des tâches devrait contenir des données.")

    def test_Journal_de_Modification(self):
        """ Vérifie que le journal des modifications s'enregistre correctement. """
        from csv import reader
        
        action = "Modification test"
        info_tache = "Test Tâche;Nouvelle description;moyenne;terminée;2025-12-31"
        Journal_de_Modification(test_chemin_journal, action, info_tache)

        with open(test_chemin_journal, 'r', encoding="utf-8") as f:
            data = list(reader(f, delimiter=';'))
        
        self.assertTrue(len(data) > 1, "Le journal des modifications devrait contenir des entrées.")

    def test_Add_tache(self):
        """ Vérifie qu'une tâche est bien ajoutée. """
        nouvelle_tache = "Nouvelle Tâche;Description ajoutée;basse;à faire;2025-12-31"
        with open(test_chemin_fichier, 'a', encoding="utf-8") as f:
            f.write(nouvelle_tache + "\n")

        with open(test_chemin_fichier, 'r', encoding="utf-8") as f:
            contenu = f.readlines()
        
        self.assertTrue(any(nouvelle_tache in ligne for ligne in contenu), "La tâche ajoutée doit être présente dans le fichier.")
        #-------------
   

    def test_Modifier_tache(self):
        """ Vérifie que la modification de tâche est bien enregistrée. """
        from io import StringIO
        import sys

        # Simulation des entrées utilisateur
        sys.stdin = StringIO("1\n1\nNouvelle Description\n")
        
        Modifier_tache(test_chemin_fichier, test_chemin_journal)

        with open(test_chemin_fichier, 'r', encoding="utf-8") as f:
            contenu = f.readlines()

        self.assertIn("Nouvelle Description", contenu[0], "La tâche modifiée doit contenir la nouvelle description.")

        sys.stdin = sys.__stdin__

    def test_supprimer_tache(self):
        """ Vérifie que la suppression de tâche fonctionne correctement. """
        from io import StringIO
        import sys

        # Simuler l'entrée utilisateur
        sys.stdin = StringIO("1\n")
        
        supprimer_tache(test_chemin_fichier)

        with open(test_chemin_fichier, 'r', encoding="utf-8") as f:
            contenu = f.readlines()
        
        self.assertEqual(len(contenu), 0, "La tâche doit être supprimée du fichier.")

        sys.stdin = sys.__stdin__
       
    def tearDown(self):
        """ Suppression des fichiers de test après chaque test. """
        if os.path.exists(test_chemin_fichier):
            os.remove(test_chemin_fichier)
        if os.path.exists(test_chemin_journal):
            os.remove(test_chemin_journal)
   

if __name__ == "__main__":
    unittest.main()
