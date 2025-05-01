# Menu general le programme commence a cet niveau 
from fonctions import *


def run_program():
    """Affiche le menu et gère les choix de l'utilisateur."""
    while True:
        try:
            print("\nGestion de Tâches")
            print("1. Créer une tâche")
            print("2. Afficher les tâches")
            print("3. Modifier une tâche")
            print("4. Rechercher une tâche")
            print("5. Journal de modification tâche")
            print("6. Supprimer une tâche")
            print("7. Quitter le programme")
            
            choix = input("\nChoisissez une option (1-7): ")  # Correction : retrait du int pour éviter les erreurs
            
            if choix == "1":
                Add_tache()
            elif choix == "2":
                Liste_des_taches()
            elif choix == "3":
                Modifier_tache(chemin_fichier, chemin_journal)
            elif choix == "4":
                Rechercher_tache()
            elif choix == "5":
                Journal_de_Modification(chemin_journal)
            elif choix == "6":
                supprimer_tache(chemin_fichier)
            elif choix == "7":
                Fin_Programme()
            else:
                print("Option invalide. Veuillez choisir une option entre 1 et 7.")
        
        except Exception as e:
            print(f'Erreur : {e}')
 
if __name__ == "__main__":
    run_program()