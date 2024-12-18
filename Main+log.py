import sys
from hashlib import sha256
from getpass import getpass
import log 

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

from hashlib import sha256

def lire_stock_global(fichier, utilisateur_clair):
    assignations = {}
    utilisateur_hash = sha256(utilisateur_clair.encode('utf-8')).hexdigest()

    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                
                utilisateur_dans_csv, nom, prix, quantite = [part.strip() for part in ligne.split(",")]
                prix = float(prix)
                quantite = int(quantite)

                #debogoage
                print(f"Vérification utilisateur : {utilisateur_dans_csv} (hashé) => comparé avec {utilisateur_hash} (hashé)")

                if utilisateur_hash == utilisateur_dans_csv:
                    if utilisateur_dans_csv not in assignations:
                        assignations[utilisateur_dans_csv] = []
                    assignations[utilisateur_dans_csv].append({
                        "nom": nom,
                        "prix": prix,
                        "stock": quantite
                    })

            except ValueError as e:
                print(f"Erreur de format dans la ligne: {ligne}. Détails de l'erreur: {e}")
                continue
    #debogoage            
    print(f"Assignations pour l'utilisateur : {assignations}")
    return assignations

def sauvegarder_stock(fichier, assignations):
    with open(fichier, "w", encoding="utf-8") as f:
        for utilisateur, produits in assignations.items():
            utilisateur_hash = sha256(utilisateur.encode('utf-8')).hexdigest()
            for produit in produits:
                f.write(f"{utilisateur_hash},{produit['nom']},{produit['prix']},{produit['stock']}\n")


def afficher_stock(stock):
    print("\n{:<40} {:<10} {:<10}".format("Nom du produit", "Prix (€)", "Stock"))
    print("=" * 60)
    for produit in stock: 
        print("{:<40} {:<10} {:<10}".format(produit["nom"], produit["prix"], produit["stock"]))

def tri_rapide(stock, key, reverse=False):
    return sorted(stock, key=lambda x: x[key], reverse=reverse)

def rechercher_produit_par_nom(stock, nom_recherche):
    resultat = [produit for produit in stock if nom_recherche.lower() in produit["nom"].lower()]
    return resultat

def ajouter_produit(stock):
    nom = input("Entrez le nom du produit : ")
    prix = float(input("Entrez le prix du produit (€) : "))
    quantite = int(input("Entrez la quantité en stock : "))
    stock.append({"nom": nom, "prix": prix, "stock": quantite})
    print(f"Produit '{nom}' ajouté avec succès !")

def supprimer_produit(stock):
    nom = input("Entrez le nom du produit à supprimer : ")
    produit_supprime = False
    for produit in stock:
        if produit["nom"].lower() == nom.lower():
            stock.remove(produit)
            produit_supprime = True
            print(f"Produit '{nom}' supprimé avec succès !")
            break
        if not produit_supprime:
            print(f"Aucun produit trouvé avec le nom '{nom}'.")

def modifier_produit(stock):
    nom = input("Entrez le nom du produit à modifier : ")
    for produit in stock:
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
    print("Connexion au système requise.")
    check, user = log.account() 
    
    if not check:
        print("Accès refusé. Vous devez vous connecter pour continuer.")
        sys.exit()  

    print(f"Bienvenue {user} ! Vous êtes connecté.")  

    assignations = lire_stock_global(fichier_produit, user)
    #debogoage
    print(f"Assignations après lecture : {assignations}")
    
    if user not in assignations:
        assignations[user] = []

    stock_utilisateur = assignations[user]
    #debogoage
    if user in assignations:
        print(f"Utilisateur trouvé dans assignations : {user}")
    else:
        print(f"Utilisateur non trouvé dans assignations : {user}")
   
    if not stock_utilisateur:

        print("Votre stock est vide. Vous pouvez commencer à ajouter des produits !")

    # Menu principal
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-5) : ")

        if choix == "1":
            #debogoage
            print(f"Stock utilisateur à afficher : {stock_utilisateur}")
            if stock_utilisateur:
                afficher_stock(stock_utilisateur)
            else:
                afficher_stock(stock_utilisateur)
                print("Votre stock est vide.")

        elif choix == "2": 
            if stock_utilisateur:
                while True:
                    afficher_tri_produit()
                    choix_tri = input("Choisissez une option (1-7) : ")
                    if choix_tri == "1":
                        stock_utilisateur = tri_rapide(stock_utilisateur, key="nom")
                    elif choix_tri == "2":
                        stock_utilisateur = tri_rapide(stock_utilisateur, key="nom", reverse=True)
                    elif choix_tri == "3":
                        stock_utilisateur = tri_rapide(stock_utilisateur, key="prix")
                    elif choix_tri == "4":
                        stock_utilisateur = tri_rapide(stock_utilisateur, key="prix", reverse=True)
                    elif choix_tri == "5":
                        stock_utilisateur = tri_rapide(stock_utilisateur, key="stock")
                    elif choix_tri == "6":
                        stock_utilisateur = tri_rapide(stock_utilisateur, key="stock", reverse=True)
                    elif choix_tri == "7":
                        break
                    afficher_stock(stock_utilisateur)
            else:
                afficher_stock(stock_utilisateur)
                print("Votre stock est vide. Ajoutez des produits avant de les trier.")

        elif choix == "3": 
            if stock_utilisateur:
                nom_recherche = input("Entrez le nom du produit à rechercher : ")
                resultats = rechercher_produit_par_nom(stock_utilisateur, nom_recherche)
                if resultats:
                    print(f"\nProduits correspondant à '{nom_recherche}' :")
                    afficher_stock(resultats)
                else:
                    print(f"\nAucun produit trouvé pour '{nom_recherche}'.")
            else:
                afficher_stock(stock_utilisateur)
                print("Votre stock est vide. Ajoutez des produits avant de rechercher.")

        elif choix == "4": 
            while True:
                afficher_menu_gestion_produits()
                choix_gestion = input("Choisissez une option (1-4) : ")
                if choix_gestion == "1":
                    ajouter_produit(stock_utilisateur)
                    sauvegarder_stock(fichier_produit, assignations)
                elif choix_gestion == "2":
                    supprimer_produit(stock_utilisateur)
                    sauvegarder_stock(fichier_produit, assignations)
                elif choix_gestion == "3":
                    modifier_produit(stock_utilisateur)
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
