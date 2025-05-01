
import os 
import csv
from datetime import datetime
import sys

chemin_fichier = r'C:\Users\DG\Desktop\Projet1\Data\FichierTache.txt' 
#    r dans le chemin permet à python de concerver tel qu'il est le chemin (car \n, \t son clés en python)
chemin_journal = r'C:\Users\DG\Desktop\Projet1\Data\JournalModif.csv' 
#
prioriteValide ={"basse", "moyenne", "haute"}
statuValid = {"a faire", "en cours", "terminée"}
'''
l'ajout des taches
'''
def Add_tache():
    while True:
        try:
            
            while True: # une tache doit avoir un nom obligatoir 
                tache_libelle = input("Titre de la tâche : ").strip()
                if tache_libelle !="":
                    break
                else:
                    print("Erreur, la tâche doit avoir un nom !")
                 
            tache_description = input("Description : ").strip()

            # Validation de la priorité
            tache_priorite = input("Priorité (basse/moyenne/haute) : ").strip().lower()
            while tache_priorite not in prioriteValide:
                print("Erreur : Priorité invalide. Veuillez choisir parmi (basse/moyenne/haute).")
                tache_priorite = input("Priorité (basse/moyenne/haute) : ").strip().lower()

            # Validation du statut
            tache_statut = input("Statut (À faire/En cours/Terminée) : ").strip().lower()
            while tache_statut not in statuValid:       
                print("Erreur : Statut invalide. Veuillez choisir parmi (À faire/En cours/Terminée).")
                tache_statut = input("Statut (À faire/En cours/Terminée) : ").strip().lower()

            # Validation de la date limite
            while True:    # la date limite ne doit pas être enterieur à la date du jour
                try:
                    tache_date_limite = datetime.strptime(input("Date limite (YYYY-MM-DD) : ").strip(), "%Y-%m-%d")
                    if tache_date_limite >= datetime.now():
                        break
                    print("Erreur : La date limite doit être dans le futur.")
                except ValueError:
                    print("Erreur : La date limite doit être au format YYYY-MM-DD.")

            # Création du répertoire(si celui ci n'est pas creer déjà) et ajout de la tâche
            if not os.path.isfile(chemin_fichier):
                
                os.makedirs(os.path.dirname(chemin_fichier), exist_ok=True)
                
            with open(chemin_fichier, 'a', encoding="utf-8", errors='replace') as taches:
                taches.write(f"{tache_libelle};{tache_description};{tache_priorite};{tache_statut};{tache_date_limite}\n")

            print("Tâche ajoutée avec succès !")
            break  # Sortie de la boucle principale

        except UnicodeDecodeError:  # gestion  des erreurs d'encodage
            print("Erreur d'encodage détectée ! Essayez de re-sauvegarder le fichier en UTF-8.")
        except Exception as e:     # gestion global des erreurs 
            print(f"Erreur : {e}")
'''
Liste des taches
'''

def Liste_des_taches():
    try:
        if not os.path.isfile(chemin_fichier):
            print("Le fichier des tâches n'existe pas.")
            return

        with open(chemin_fichier, 'r', encoding="utf-8", errors='replace') as fichier:
            lignes = fichier.readlines()

        if not lignes:
            print("Aucune tâche trouvée.")
            return
        
        print("\n_____Liste des tâches_______________")
        for i, ligne in enumerate(lignes):
            try:
                tache = ligne.strip().split(";")  # Séparer les données avec ';'
                
                if len(tache) < 5:                  # pour vérifier que toutes les informations sont bien présentes
                    raise ValueError(f" Erreur: {i+1}, données incomplètes.")
                    
                print(f"\n Tâche No   : ({i+1})")
                print(f"- Titre       : {tache[0]}")
                print(f"- Description : {tache[1]}")
                print(f"- Priorité    : {tache[2]}")
                print(f"- Statut      : {tache[3]}")
                print(f"- Date limite : {tache[4]}")
                print('___________________________________')
                
            except ValueError as val:
                print(f"Erreur :{val}")
                
    except FileNotFoundError as F:
        print(f"Erreur :{F}")  # Gestion pour fichier introuvable
    except ValueError as V:   
        print(f"Erreur :{V}")  # gestion pour fichier vide ou des erreurs globales
    except UnicodeDecodeError: # Gestion d'encodage 
            print("Erreur d'encodage détectée ! Essayez de re-sauvegarder le fichier en UTF-8.")
    except Exception as e:
        print(f"Erreur d'accès au fichier : {e}") #pour des erreurs imprévus

'''
Trace de modification
'''
def Journal_de_Modification(chemin_journal, action="", tache_info=""):
    try:
        date_modification = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fichier_existe = os.path.isfile(chemin_journal)

        # Si une modification est enregistrée, l'ajouter au journal
        if action and tache_info:
            with open(chemin_journal, 'a', newline='', encoding="utf-8", errors='replace') as fichier:
                writer = csv.writer(fichier, delimiter=';')
                if not fichier_existe:
                    writer.writerow(["Date de modification", "Action", "Informations sur la tâche"])
                
                writer.writerow([date_modification, action, tache_info])
            print("Modification enregistrée dans le journal.")

        # Affichage des modifications si appelé sans action
        if not action:
            if not fichier_existe or os.stat(chemin_journal).st_size == 0:
                print("Aucune modification enregistrée.")
                return

            print("\n Journal des Modifications :\n")
            with open(chemin_journal, 'r', encoding="utf-8") as fichier:
                reader = csv.reader(fichier, delimiter=';')
                next(reader)  # Ignorer l'en-tête
                
                for ligne in reader:
                    print(f"{ligne[0]} | {ligne[1]} |  {ligne[2]}")
                print("\n___________________________")
                
    except UnicodeDecodeError:
        print("Erreur d'encodage détectée ! Essayez de re-sauvegarder le fichier en UTF-8.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement ou l'affichage du journal : {e}")

'''
Modification des tâches
'''
def Modifier_tache(chemin_fichier, chemin_journal):
    """Modifier une tâche spécifique en simulant les entrées utilisateur correctement."""
    try:
        if not os.path.isfile(chemin_fichier):
            print("Le fichier des tâches n'existe pas.")
            return

        with open(chemin_fichier, 'r', encoding="utf-8", errors='replace') as fichier:
            taches = fichier.readlines()

        if not taches:
            print("Aucune tâche trouvée.")
            return
        
        print("\nListe des tâches disponibles :")
        for i, ligne in enumerate(taches):
            print(f"{i+1}. {ligne.strip()}")

        choix = int(input("\nEntrez le numéro de la tâche à modifier : ")) - 1    
        if choix < 0 or choix >= len(taches):
            print("Numéro de tâche invalide.")
            return

        tache = taches[choix].strip().split(";")
        
        print("\nQue voulez-vous modifier ?")
        print("1. Description\n2. Statut")
        champ = int(input("Choisissez une option : ")) 

        ancienne_valeur = tache[1] if champ == 1 else tache[3]

        if champ == 1:
            nouvelle_valeur = input("Entrez la nouvelle description : ")
            tache[1] = nouvelle_valeur  # Pas d'exigence pour la description
            
        elif champ == 2:
            while True:  
                nouvelle_valeur = input("Entrer le nouveau statut (À faire/En cours/Terminée) : ").lower()
                if nouvelle_valeur in statuValid:
                    tache[3] = nouvelle_valeur
                    break  
                else:  
                    print("Erreur : Statut invalide. Veuillez choisir parmi (À faire/En cours/Terminée).")           

        else:
            print("Option invalide.")
            return

        taches[choix] = ";".join(tache) + "\n"

        with open(chemin_fichier, 'w', encoding="utf-8", errors='replace') as fichier:
            fichier.writelines(taches)

        print("Tâche modifiée avec succès !")

        # Ajout dans le journal des modifications
        action = f"Modification de la tâche No {choix+1}: {ancienne_valeur} -> {nouvelle_valeur}"
        Journal_de_Modification(chemin_journal, action, ";".join(tache))

    except FileNotFoundError as F:
        print(f"Erreur : {F}")
    except ValueError:
        print("Veuillez entrer un nombre valide.")
    except UnicodeDecodeError: # Gestion d'encodage
        print("Erreur d'encodage détectée ! Essayez de re-sauvegarder le fichier en UTF-8.")
    except Exception as e:
        print(f"Erreur : {e}")
"""
recherche de tache(Nom ou description )
"""
def Rechercher_tache():
    try:
        mot_cle = input("Entrez le mot-clé à rechercher (nom ou description ): ").lower()
        trouve = False
        
        if not os.path.isfile(chemin_fichier):
            print("Le fichier des tâches n'existe pas.")
            return
        
        with open(chemin_fichier, 'r',encoding="utf-8", errors='replace') as fichier:
            taches = fichier.readlines()
            
        if not taches:
            print("Aucune tâche trouvée.")
            return
        
        print("\n Résultat de la recherche")
        for i, ligne in enumerate(taches):
            try:
                tache = ligne.strip().split(";")
                if len(tache)<5:
                    raise ValueError(f"Erreur de format sur la tache {i+1}, données incomplètes")
                    
                
                if mot_cle in tache[0].lower() or mot_cle in tache[1].lower():
                    trouve = True
                    print(f"\nTâche No:{i+1}:")
                    print(f"- Titre: {tache[0]}")
                    print(f"- Description: {tache[1]}")
                    print(f"- Priorité: {tache[2]}")
                    print(f"- Statut: {tache[3]}")
                    print(f"- Date limite: {tache[4]}")
                    print('___________________________')
                    
            except ValueError as val:
                print(f'Erreur lors du traitemen de tache {i+1} : {val}')
        if not trouve:
                print("Aucune tâche trouvée.")     
                
    except FileNotFoundError as F:
        print(f"Erreur :{F}") # Gestion pour fichier introuvable
    except Exception as e:
        print(f"Erreur d'accès au fichier : {e}") #pour des erreurs imprévus
        
'''
la fonction supprimer_tache va nous permetre de supprimer une tache()
'''
def supprimer_tache(chemin_fichier):
    """ Supprime une tâche spécifique du fichier. """
    if not os.path.isfile(chemin_fichier):
        print("Le fichier des tâches n'existe pas.")
        return

    try:
        with open(chemin_fichier, 'r+', encoding="utf-8", errors='replace') as fichier:
            taches = fichier.readlines()
            if not taches:
                print("Aucune tâche trouvée.")
                return

            print("\nListe des tâches disponibles :")
            for i, ligne in enumerate(taches, 1):
                print(f"{i}. {ligne.strip()}")

            try:
                num_tache = int(input("\nEntrez le numéro de la tâche à supprimer : ")) - 1
                if not (0 <= num_tache < len(taches)):
                    print("Numéro de tâche invalide.")
                    return
            except ValueError:
                print("Veuillez entrer un numéro valide.")
                return

            print(f"Suppression de la tâche No {num_tache + 1}: {taches[num_tache].strip()}")
            del taches[num_tache]  # Suppression de la tâche

            fichier.seek(0)
            fichier.truncate()
            fichier.writelines(taches)  # Réécriture du fichier

            print("Tâche supprimée avec succès.")

    except UnicodeDecodeError:
        print("Erreur d'encodage détectée ! Essayez de re-sauvegarder le fichier en UTF-8.")
    except Exception as e:
        print(f"Erreur d'accès au fichier : {e}")
        
def Fin_Programme():
    print("Merci! À bientôt!")
    sys.exit()   
    
