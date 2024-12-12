import sys

def afficher_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Afficher le stock")
    print("2. Filtre stock")
    print("3. Rechercher un produit")
    print("4. Gestion produits")
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
    print("7. Retour au menu pricnipal")
    print("====================")

#===========================================================================================================

def lire_stock(fichier):
    stock = []
    with open(fichier, "r", encoding="utf-8") as f: 
        for ligne in f: 
            nom, prix, quantite = ligne.strip().split(",")
            stock.append({
                "nom": nom,
                "prix": float(prix),
                "stock": int(quantite) 
            })
    return stock

def sauvegarder_stock(fichier, stock):
    with open(fichier, "w", encoding="utf-8") as f:
        for produit in stock:
            f.write(f"{produit['nom']},{produit['prix']},{produit['stock']}\n")

def afficher_stock(stock):
    print("\n{:<40} {:<10} {:<10}".format("Nom du produit", "Prix (€)", "Stock"))
    print("=" * 60)
    for produit in stock: 
        print("{:<40} {:<10} {:<10}".format(produit["nom"], produit["prix"], produit["stock"]))

def tri_par_nom(stock): #Ordre croissant 
    return sorted(stock, key=lambda produit: produit["nom"])
def tri_par_nom_d(stock): #Ordre décroissant
    return sorted(stock, key=lambda produit: produit["nom"], reverse=True)

def tri_par_prix(stock):#Ordre croissant 
    return sorted(stock, key=lambda produit: produit["prix"])
def tri_par_prix_d(stock):#Ordre décroissant
    return sorted(stock, key=lambda produit: produit["prix"], reverse=True) 

def tri_par_quantite(stock):#Ordre croisant 
    return sorted(stock, key=lambda produit: produit["stock"])
def tri_par_quantite_d(stock):#Ordre décroissant
    return sorted(stock, key=lambda produit: produit["stock"], reverse=True)

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

#===========================================================================================================

if __name__ == "__main__":
    fichier_stock = "stock.txt"
    stock = lire_stock(fichier_stock)

    while True:
        #Pour afficher menuji
        afficher_menu()
        choix = input("Choisissez une option (1-5) : ")
        
        #Poir afficher stock 
        if choix == "1":
            afficher_stock(stock)
        #Pour afficher le triu
        elif choix == "2": 
            while True: 
                afficher_tri_produit()
                choix_tri = input("Choisissez une option (1-7) : ")
                if choix_tri == "1":
                    stock = tri_par_nom(stock)
                    print("\nStock trié par orde alphabétique croissant")
                    afficher_stock(stock)
                elif choix_tri == "2":
                    stock = tri_par_nom_d(stock)
                    print("\nStock trié par orde alphabétique décroissant")
                    afficher_stock(stock)
                elif choix_tri == "3":
                    stock = tri_par_prix(stock)
                    print("\nStock trié par prix en orde croissant")
                    afficher_stock(stock)
                elif choix_tri == "4":
                    stock = tri_par_prix_d(stock)
                    print("\nStock trié par prix en orde décroissant")
                    afficher_stock(stock)
                elif choix_tri == "5":
                    stock = tri_par_quantite(stock)
                    print("\nStock trié par quantité en orde croissant")
                    afficher_stock(stock)
                elif choix_tri == "6":
                    stock = tri_par_quantite_d(stock)
                    print("\nStock trié par quantité en orde décroissant")
                    afficher_stock(stock)
                elif choix_tri == "7":
                    break
                else : 
                    print ("Option invalide. Veuillez chosir une option entre 1 et 7 !")
        #Pour recherche de produit            
        elif choix == "3":
            nom_recherche = input("Entrez le nom du produit à rechercher : ")
            resultats = rechercher_produit_par_nom(stock, nom_recherche)
            if resultats:
                print(f"\nProduits correspondant à '{nom_recherche}' :")
                afficher_stock(resultats)
            else:
                print(f"\nAucun produit trouvé pour '{nom_recherche}'.")
        #Pour affichjer gestion produit donc ajout supp modif 
        elif choix == "4":
            while True:
                afficher_menu_gestion_produits()
                choix_gestion = input("Choisissez une option (1-4) : ")
                if choix_gestion == "1":
                    ajouter_produit(stock)
                elif choix_gestion == "2":
                    supprimer_produit(stock)
                elif choix_gestion == "3":
                    modifier_produit(stock)
                elif choix_gestion == "4":
                    break 
                else:
                    print("Option invalide. Veuillez choisir une options entre 1 et 4 !")
        elif choix == "5":
            sauvegarder_stock(fichier_stock, stock)
            print("À bientôt !")
            sys.exit()
        else:
            print("Option invalide. Veuillez choisir une option entre 1 et 5 !")
