import sys
from hashlib import sha256
from getpass import getpass
import log 
import pandas as pd

def afficher_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Afficher le stock")
    print("2. Filtrer le stock")
    print("3. Rechercher un produit")
    print("4. Gestion des produits")
    print("5. Quitter")
    print("======================")

def afficher_menu_gestion_produits(): 
    print("\n=== GESTION DES PRODUITS ===")
    print("1. Ajouter un produit")
    print("2. Supprimer un produit")
    print("3. Modifier un produit")
    print("4. Retour au menu principal")
    print("=============================")

def afficher_tri_produit(): 
    print("\n=== TRI PRODUITS ===")
    print("1. Trier le stock par nom (ordre alphabétique croissant)")
    print("2. Trier le stock par nom (ordre alphabétique décroissant)")
    print("3. Trier le stock par prix (ordre croissant)")
    print("4. Trier le stock par prix (ordre décroissant)")
    print("5. Trier le stock par quantité (ordre croissant)")
    print("6. Trier le stock par quantité (ordre décroissant)")
    print("7. Retour au menu principal")
    print("====================")

#===========================================================================================================


def lire_stock_global(fichier, utilisateur_clair):
    assignations = {}
    utilisateur_hash = sha256(utilisateur_clair.strip().encode('utf-8')).hexdigest()
    
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    utilisateur_dans_csv, nom, prix, quantite = [part.strip() for part in ligne.split(",")]
                    prix = float(prix)
                    quantite = int(quantite)

                    if utilisateur_hash == utilisateur_dans_csv:
                        if utilisateur_dans_csv not in assignations:
                            assignations[utilisateur_dans_csv] = []
                        assignations[utilisateur_dans_csv].append({
                            "nom": nom,
                            "prix": prix,
                            "stock": quantite
                        })
                except ValueError as e:
                    print(f"Erreur dans la ligne : {ligne}. Détails : {e}")
    except FileNotFoundError:
        print(f"Fichier '{fichier}' introuvable.")
    
    return assignations

def sauvegarder_stock(fichier, assignations):
    lignes_existantes = set()
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                lignes_existantes.add(ligne.strip()) 
    except FileNotFoundError:
        pass 
    with open(fichier, "a", encoding="utf-8") as f:
        for utilisateur, produits in assignations.items():
            for produit in produits:
                ligne = f"{utilisateur},{produit['nom']},{produit['prix']},{produit['stock']}\n"
                if ligne.strip() not in lignes_existantes:
                    f.write(ligne)
                    lignes_existantes.add(ligne.strip())

def afficher_stock(assignations, utilisateur_hash):
    if utilisateur_hash in assignations:
        produits = assignations[utilisateur_hash]
        if produits:
            print("\n{:<40} {:<10} {:<10}".format("Nom du produit", "Prix (€)", "Stock"))
            print("=" * 60)
            for produit in produits:
                print("{:<40} {:<10} {:<10}".format(produit["nom"], produit["prix"], produit["stock"]))
        else:
            print("Votre stock est vide. Vous pouvez commencer à ajouter des produits !")
    else:
        print("Utilisateur non trouvé.")

def tri_rapide(stock, key, reverse=False):
    return sorted(stock, key=lambda x: x[key], reverse=reverse)

def rechercher_produit_par_nom(stock, nom_recherche):
    resultat = [produit for produit in stock if nom_recherche.lower() in produit["nom"].lower()]
    return resultat

def ajouter_produit(assignations, utilisateur):
    nom = input("Entrez le nom du produit : ")
    try:
        prix = float(input("Entrez le prix du produit (€) : "))
        quantite = int(input("Entrez la quantité en stock : "))
    except ValueError:
        print("Prix ou quantité invalide. Essayez encore.")
        return
    if utilisateur not in assignations:
        assignations[utilisateur] = []
    assignations[utilisateur].append({"nom": nom, "prix": prix, "stock": quantite})
    print(f"Produit '{nom}' ajouté avec succès !")

def supprimer_produit(assignations, utilisateur):
    if utilisateur not in assignations or not assignations[utilisateur]:
        print("Votre stock est vide. Aucun produit à supprimer.")
        return

    nom = input("Entrez le nom du produit à supprimer : ")
    produits = assignations[utilisateur]
    produit_supprime = False

    for produit in produits:
        if produit["nom"].lower() == nom.lower():
            produits.remove(produit)
            produit_supprime = True
            print(f"Produit '{nom}' supprimé avec succès !")
            break

    if not produit_supprime:
        print(f"Aucun produit trouvé avec le nom '{nom}'.")


def modifier_produit(assignations, utilisateur ):
    if utilisateur not in assignations or not assignations[utilisateur]:
        print("Votre stock est vide. Aucun produit à modifier.")
        return
    nom = input("Entrez le nom du produit à modifier : ")
    for produit in produits:
        if produit["nom"].lower() == nom.lower():
            print(f"Produit trouvé: {produit['nom']}")
            choix = input("Que voulez-vous modifier ? (1. Nom, 2. Prix, 3. Quantité) : ")
            if choix == "1":
                nouveau_nom = input("Entrez le nouveau nom : ")
                produit["nom"] = nouveau_nom
                print(f"Nom modifié en '{nouveau_nom}'")
            elif choix == "2":
                nouveau_prix = float(input("Entrez le nouveau prix : "))
                produit["prix"] = nouveau_prix
                print(f"Prix modifié à {nouveau_prix}€")
            elif choix == "3":
                nouvelle_quantite = int(input("Entrez la nouvelle quantité : "))
                produit["stock"] = nouvelle_quantite
                print(f"Quantité modifiée à {nouvelle_quantite}")
            else:
                print("Choix invalide.")
            return
    print(f"Aucun produit trouvé avec le nom '{nom}'.")


def initialiser_stock_utilisateur(assignations, utilisateur):
    if utilisateur not in assignations:
        assignations[utilisateur] = []

#===========================================================================================================

if __name__ == "__main__":
    fichier_produit = "assignations_stock.csv"
    fichier_compromis = 'C:/Users/rmeney/Documents/GitHub/rockyou-sha256.txt'
    print("Connexion au système requise.")
    check, user = log.account()

    if not check:
        print("Accès refusé. Vous devez vous connecter pour continuer.")
        sys.exit()  
    utilisateur_hash = sha256(user.strip().encode('utf-8')).hexdigest()
    print(f"Bienvenue {user} ! Vous êtes connecté.")  

    assignations = lire_stock_global(fichier_produit, user)


    # Menu principal
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
                afficher_stock(assignations, utilisateur_hash)
        elif choix == "2": 
            produits = assignations.get(utilisateur_hash, [])
            if produits:
                afficher_tri_produit()
                choix_tri = input("Choisissez une option (1-7) : ")
                key_map = {"1": "nom", "2": "nom", "3": "prix", "4": "prix", "5": "stock", "6": "stock"}
                reverse_map = {"1": False, "2": True, "3": False, "4": True, "5": False, "6": True}
                if choix_tri in key_map:
                    produits = tri_rapide(produits, key=key_map[choix_tri], reverse=reverse_map[choix_tri])
                    assignations[utilisateur_hash] = produits
                    afficher_stock(assignations, utilisateur_hash)
            else:
                print("Votre stock est vide.")

        elif choix == "3": 
            produits = assignations.get(utilisateur_hash, [])
            if produits:
                nom_recherche = input("Entrez le nom du produit à rechercher : ")
                resultats = rechercher_produit_par_nom(produits, nom_recherche)
                if resultats:
                    print(f"\nProduits correspondant à '{nom_recherche}' :")
                    print("\n{:<40} {:<10} {:<10}".format("Nom du produit", "Prix (€)", "Stock"))
                    print("=" * 60)
                    for produit in resultats:
                        print("{:<40} {:<10} {:<10}".format(produit["nom"], produit["prix"], produit["stock"]))
                else:
                    print(f"\nAucun produit trouvé pour '{nom_recherche}'.")
            else:
                print("Votre stock est vide. Ajoutez des produits avant de rechercher.")

        elif choix == "4": 
            while True:
                afficher_menu_gestion_produits()
                choix_gestion = input("Choisissez une option (1-4) : ")
                if choix_gestion == "1":
                    ajouter_produit(assignations, utilisateur_hash)
                    sauvegarder_stock(fichier_produit, assignations)
                elif choix_gestion == "2":
                    supprimer_produit(assignations, utilisateur_hash)
                    sauvegarder_stock(fichier_produit, assignations)
                elif choix_gestion == "3":
                    modifier_produit(assignations, utilisateur_hash)
                    sauvegarder_stock(fichier_produit, assignations)
                elif choix_gestion == "4":
                    break
                else:
                    print("Option invalide. Veuillez choisir une option entre 1 et 4 !")

        elif choix == "5":
            sauvegarder_stock(fichier_produit, assignations)
            print("À bientôt !")
            sys.exit()
        else:
            print("Option invalide. Veuillez choisir une option entre 1 et 5 !")
