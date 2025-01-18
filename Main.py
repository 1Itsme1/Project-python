import sys
from hashlib import sha256
from getpass import getpass
import log 
import requests
import hashlib 
import csv 
from datetime import datetime
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as MessageBox

"""
def afficher_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("0. Compte")
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

def afficher_compte(): 
    print("\n=== GESTION COMPTE ===")
    print ("1. Changer de mot de passe")
    print ("2. Supprimer mon compte /!\\")
    print("3. Retour au menu principal")
    print("====================")
"""
#===========================================================================================================

def enregistrer_historique_requete(fichier_historique, utilisateur, action):
    try:
        with open(fichier_historique, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if f.tell() == 0:
                writer.writerow(["Utilisateur", "Mot de passe haché", "Timestamp"])
            writer.writerow([utilisateur, action, timestamp])

    except Exception as e:
        print(f"Erreur lors de l'enregistrement de l'historique : {e}")

#===========================================================================================================
def lire_stock_global_all(fichier_produit):
    stock_global = []
    
    try:
        with open(fichier_produit, "r", encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    utilisateur_dans_csv, nom, prix, quantite = [part.strip() for part in ligne.split(",")]
                    prix = float(prix)
                    quantite = int(quantite)

                    stock_global.append({
                        "utilisateur": utilisateur_dans_csv,
                        "nom": nom,
                        "prix": prix,
                        "stock": quantite
                    })
                except ValueError as e:
                    print(f"Erreur dans la ligne : {ligne}. Détails : {e}")
    except FileNotFoundError:
        print(f"Fichier '{fichier_produit}' introuvable.")
    
    return stock_global

#===========================================================================================================

def lire_stock_global(fichier, user):
    assignations = {}
    utilisateur_hash = sha256(user.strip().encode('utf-8')).hexdigest()
    
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

#===========================================================================================================
def sauvegarder_stock(fichier_produit, assignations):
    
    lignes_anciennes = {}
    try:
        with open(fichier_produit, "r", encoding="utf-8") as f:
            for i,ligne in enumerate(f):
                ligne = ligne.strip()
                if ligne:
                    if i == 0 and "utilisateur" in ligne.lower():
                        continue
                    utilisateur, nom, prix, quantite = ligne.split(",")
                    if utilisateur not in lignes_anciennes:
                        lignes_anciennes[utilisateur] = []
                    lignes_anciennes[utilisateur].append({
                        "nom": nom,
                        "prix": float(prix),
                        "stock": int(quantite)
                    })
    except FileNotFoundError:
        pass

    for utilisateur, produits in assignations.items():
        lignes_anciennes[utilisateur] = produits

    with open(fichier_produit, "w", encoding="utf-8") as f:
        f.write("utilisateur,nom,prix,stock\n")
        for utilisateur, produits in lignes_anciennes.items():
            for produit in produits:
                f.write(f"{utilisateur},{produit['nom']},{produit['prix']},{produit['stock']}\n")

#===========================================================================================================
"""
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
        print("Votre stock est vide. Vous pouvez commencer à ajouter des produits !")
"""       
#===========================================================================================================

def tri_rapide(stock, key, reverse=False):
    return sorted(stock, key=lambda x: x[key], reverse=reverse)

#===========================================================================================================
def rechercher_produit_par_nom(stock, nom_recherche):
    resultat = [produit for produit in stock if nom_recherche.lower() in produit["nom"].lower()]
    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Recherche d'un produit")
    return resultat


#===========================================================================================================
"""
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
    sauvegarder_stock(fichier_produit, assignations)

#===========================================================================================================
def supprimer_produit(assignations, utilisateur):
    if utilisateur not in assignations or not assignations[utilisateur]:
        print("Votre stock est vide. Aucun produit à supprimer.")
        return

    nom = input("Entrez le nom du produit à supprimer : ")
    produits = assignations[utilisateur]
    produit_supprime = False

    
    for produit in produits[:]:  
        if produit["nom"].lower() == nom.lower():
            produits.remove(produit)
            produit_supprime = True
            print(f"Produit '{nom}' supprimé avec succès !")
    
            break

    if not produit_supprime:
        print(f"Aucun produit trouvé avec le nom '{nom}'.")
    else:
        sauvegarder_stock(fichier_produit, assignations)  
#===========================================================================================================
def modifier_produit(assignations, utilisateur):
    if utilisateur not in assignations or not assignations[utilisateur]:
        print("Votre stock est vide. Aucun produit à modifier.")
        return
    
    nom = input("Entrez le nom du produit à modifier : ")
    produits = assignations[utilisateur]

    for produit in produits:
        if produit["nom"].lower() == nom.lower():
            print(f"Produit trouvé: {produit['nom']}")
            choix = input("Que voulez-vous modifier ? (1. Nom, 2. Prix, 3. Quantité) : ")
            if choix == "1":
                nouveau_nom = input("Entrez le nouveau nom : ")
                produit["nom"] = nouveau_nom
                print(f"Nom modifié en '{nouveau_nom}'")
                enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Modification nom du produit")
            elif choix == "2":
                try:
                    nouveau_prix = float(input("Entrez le nouveau prix : "))
                    produit["prix"] = nouveau_prix
                    print(f"Prix modifié à {nouveau_prix}€")
                    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Modification prix du produit")
                except ValueError:
                    print("Le prix doit être un nombre valide.")
            elif choix == "3":
                try:
                    nouvelle_quantite = int(input("Entrez la nouvelle quantité : "))
                    produit["stock"] = nouvelle_quantite
                    print(f"Quantité modifiée à {nouvelle_quantite}")
                    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Modification quantité du produit")
                except ValueError:
                    print("La quantité doit être un nombre entier valide.")
            else:
                print("Choix invalide.")
            sauvegarder_stock(fichier_produit, assignations)
            return
    
    print(f"Aucun produit trouvé avec le nom '{nom}'.")
#===========================================================================================================
def initialiser_stock_utilisateur(assignations, utilisateur):
    if utilisateur not in assignations:
        assignations[utilisateur] = []
"""
#===========================================================================================================
def enregistrer_mot_de_passe_compromis(fichier_compromis, utilisateur_hash, mot_de_passe):
    try:
        with open(fichier_compromis, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mot_de_passe_hache = hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()
            
            if f.tell() == 0:
                writer.writerow(["Utilisateur", "Mot de passe haché", "Timestamp"])
            writer.writerow([utilisateur_hash, mot_de_passe_hache, timestamp])

    except Exception as e:
        print(f"Erreur lors de l'enregistrement du mot de passe compromis : {e}")
#===========================================================================================================

#import smtplib
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart

#def envoyer_email_notification():

#===========================================================================================================
def verifier_password(password, utilisateur_hash):

    try:
        
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_hash[:5]  
        suffix = sha1_hash[5:]  

        
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)

       
        if response.status_code != 200:
            raise RuntimeError(f"Erreur de connexion à l'API : {response.status_code}")

        
        found = False
        hashes = (line.split(':') for line in response.text.splitlines())
        for returned_suffix, count in hashes:
            if returned_suffix == suffix:
                MessageBox.showwarning(
                    "Mot de passe compromis",
                    f"Votre mot de passe a été trouvé {count} fois dans des fuites !\n"
                    "Nous vous recommandons de le changer rapidement dans la rubrique Compte."
                )
                found = True
                enregistrer_mot_de_passe_compromis("./Data/historique_compromissions.csv", utilisateur_hash, password)
                break

        if not found:
            MessageBox.showinfo("Mot de passe sécurisé", "Votre mot de passe est bien sécurisé")
    
    except RuntimeError as e:
        MessageBox.showerror("Erreur", f"Une erreur s'est produite : {e}")
    except Exception as e:
        MessageBox.showerror("Erreur", f"Une erreur inattendue s'est produite : {e}")

#===========================================================================================================
import csv
import hashlib
import tkinter as tk
from tkinter import messagebox
import base64
import os
def generer_salt():
    return base64.b64encode(os.urandom(16)).decode('utf-8')

def changer_mot_de_passe_graphique(fichier_usernames_passwords,utilisateur_hash, fenetre):
    
    with open(fichier_usernames_passwords, 'r', encoding='utf-8') as csvfilepass:
        reader = csv.reader(csvfilepass, delimiter=',')
        next(reader, None) 
        utilisateurs = list(reader)

    utilisateur_data = None
    for row in utilisateurs:
        if row[0] == utilisateur_hash:  
            utilisateur_data = row
            break

    if not utilisateur_data:
        messagebox.showerror("Erreur", "Utilisateur introuvable.")
        return

    
    def valider_nouveau_mot_de_passe():
       
        nouveau_mot_de_passe = entry_nouveau_mdp.get()
        confirmer_mot_de_passe = entry_confirmer_mdp.get()

       
        if nouveau_mot_de_passe != confirmer_mot_de_passe:
            messagebox.showwarning("Attention", "Les mots de passe ne correspondent pas.")
            return

        if len(nouveau_mot_de_passe) < 8 or not any(c.isdigit() for c in nouveau_mot_de_passe) or not any(c.isupper() for c in nouveau_mot_de_passe):
            messagebox.showwarning("Attention", "Le mot de passe doit comporter au moins 8 caractères, inclure un chiffre et une majuscule.")
            return

        
        nouveau_salt = generer_salt()
        hash_nouveau_mot_de_passe = hashlib.sha256((nouveau_salt + nouveau_mot_de_passe).encode('utf-8')).hexdigest()

        
        utilisateur_data[1] = nouveau_salt
        utilisateur_data[2] = hash_nouveau_mot_de_passe

        
        with open(fichier_usernames_passwords, 'w', encoding='utf-8', newline='') as csvfilepass:
            writer = csv.writer(csvfilepass, delimiter=',')
            writer.writerow(["Utilisateur", "Salt", "Mot de passe"])

            for row in utilisateurs:
                writer.writerow(row)

       
        messagebox.showinfo("Succès", "Mot de passe mis à jour avec succès !")
        fenetre_changement_mdp.destroy()

   
    fenetre_changement_mdp = tk.Toplevel(fenetre)
    fenetre_changement_mdp.title("Changer le mot de passe")
    fenetre_changement_mdp.geometry("400x300")

    
    label_nouveau_mdp = tk.Label(fenetre_changement_mdp, text="Nouveau mot de passe")
    label_nouveau_mdp.pack(pady=10)

    entry_nouveau_mdp = tk.Entry(fenetre_changement_mdp, show="*")
    entry_nouveau_mdp.pack(pady=5)

    label_confirmer_mdp = tk.Label(fenetre_changement_mdp, text="Confirmer le mot de passe")
    label_confirmer_mdp.pack(pady=10)

    entry_confirmer_mdp = tk.Entry(fenetre_changement_mdp, show="*")
    entry_confirmer_mdp.pack(pady=5)

    
    bouton_valider = tk.Button(fenetre_changement_mdp, text="Valider", command=valider_nouveau_mot_de_passe)
    bouton_valider.pack(pady=20)


#===========================================================================================================
def suppression_compte(fichier_usernames_passwords, fichier_produit, utilisateur_hash, verifier_mot_de_passe, fenetre):
    
    with open(fichier_usernames_passwords, 'r', encoding='utf-8') as csvfilepass:
        reader = csv.reader(csvfilepass, delimiter=',')
        header_users = next(reader, None)
        utilisateurs = list(reader)

    utilisateur_data = next((row for row in utilisateurs if row[0] == utilisateur_hash), None)
    if not utilisateur_data:
        messagebox.showerror("Erreur", "Utilisateur introuvable.")
        return

   
    confirmation = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer votre compte ?")
    if not confirmation:
        messagebox.showinfo("Annulation", "Suppression annulée.")
        return

    def valider_mot_de_passe():
        mot_de_passe = mot_de_passe_entry.get()
        if not verifier_mot_de_passe(utilisateur_data[1], utilisateur_data[2], mot_de_passe):
            messagebox.showerror("Erreur", "Mot de passe incorrect.")
            return
        else:
            supprimer_utilisateur(utilisateur_data)
            suppression_window.destroy()

    
    suppression_window = tk.Toplevel(fenetre)
    suppression_window.title("Vérification du mot de passe")

    label_mdp = tk.Label(suppression_window, text="Entrez votre mot de passe pour confirmer :")
    label_mdp.pack(pady=10)

    mot_de_passe_entry = tk.Entry(suppression_window, show="*")
    mot_de_passe_entry.pack(pady=10)

    bouton_valider_mdp = tk.Button(suppression_window, text="Valider", command=valider_mot_de_passe)
    bouton_valider_mdp.pack(pady=10)

    suppression_window.mainloop()

def supprimer_utilisateur(utilisateur_data):

    fichier_usernames_passwords = "./DATA/usernames_passwords.csv"
    fichier_produit = "./DATA/assignations_stock.csv"
    
    
    with open(fichier_usernames_passwords, 'r', encoding='utf-8') as csvfilepass:
        reader = csv.reader(csvfilepass, delimiter=',')
        header_users = next(reader, None)
        utilisateurs = list(reader)

    utilisateurs_sans_compte = [row for row in utilisateurs if row[0] != utilisateur_data[0]]
    
    with open(fichier_usernames_passwords, 'w', encoding='utf-8', newline='') as csvfilepass:
        writer = csv.writer(csvfilepass, delimiter=',')
        if header_users:
            writer.writerow(header_users)
        writer.writerows(utilisateurs_sans_compte)

    
    with open(fichier_produit, 'r', encoding='utf-8') as csvfileprod:
        reader = csv.reader(csvfileprod, delimiter=',')
        header_products = next(reader, None)
        produits = list(reader)

    produits_restants = [row for row in produits if row[0] != utilisateur_data[0]]

    with open(fichier_produit, 'w', encoding='utf-8', newline='') as csvfileprod:
        writer = csv.writer(csvfileprod, delimiter=',')
        if header_products:
            writer.writerow(header_products)
        writer.writerows(produits_restants)

    messagebox.showinfo("Succès", "Votre compte et les données associées ont été supprimés avec succès.")

def verifier_mot_de_passe(salt, mot_de_passe_hash, mot_de_passe):
    
    hash_calculé = hashlib.sha256((salt + mot_de_passe).encode('utf-8')).hexdigest()
    return hash_calculé == mot_de_passe_hash     
        
#===========================================================================================================
"""""
if __name__ == "__main__":
    fichier_produit = "./Data/assignations_stock.csv"
    #fichier_listeCompromis = 'C:/Users/rmeney/Documents/GitHub/rockyou-sha256.txt'
    fichier_compromis = "./DATA/historique_compromissions.csv"
    fichier_historique = "./DATA/historique_requete.csv"
    fichier_usernames_passwords = "./Data/usernames_passwords.csv"
   
    print("Connexion au système requise.")
    check, user = log.account()
    if sys.exit():
        utilisateur_hash = sha256(user.strip().encode('utf-8')).hexdigest()
        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Deconnexion")
    if not check:
        utilisateur_hash = sha256(user.strip().encode('utf-8')).hexdigest()
        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Connexion réussi")
        print("Accès refusé. \nSi vous n'avez pas de compte créez en un ! \nSinon l'email ou le mot de passe est incorrect !")
        sys.exit()
    
    utilisateur_hash = sha256(user.strip().encode('utf-8')).hexdigest()
    email = user
    name_avant_arobase = email.split('@')[0]
    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Connexion réussi")
    print(f"Bienvenue {name_avant_arobase} ! Vous êtes connecté.")  

    assignations = lire_stock_global(fichier_produit, user)
"""
"""""
    # Menu principal

    while True:
        afficher_menu()
        choix = input("Choisissez une option (0-5) : ")

        if choix == "0":
            while True:
                afficher_compte()
                choix_compte = input("Choisissez une option (1-3) : ")
                if choix_compte == "1":
                    changer_mot_de_passe(fichier_usernames_passwords, utilisateur_hash)
                    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Changemenet de mot de passe")
                elif choix_compte == "2":
                    suppression_compte(fichier_usernames_passwords, fichier_produit, utilisateur_hash, verifier_mot_de_passe)
                    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Suppression du compte")
                    sys.exit() 
                elif choix_compte == "3":
                    break
                else:
                    print("Option invalide. Veuillez choisir une options entre 1 et 2.")

        elif choix == "1":
                afficher_stock(assignations, utilisateur_hash)
                enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Affichage du stock")
              
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
                    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Tri du stock")
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
                    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Ajout d'un produit")
                elif choix_gestion == "2":
                    supprimer_produit(assignations, utilisateur_hash)
                    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Suppression d'un produit")
                elif choix_gestion == "3":
                    modifier_produit(assignations, utilisateur_hash)
                    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Modification produit")
                elif choix_gestion == "4":
                    break
                else:
                    print("Option invalide. Veuillez choisir une option entre 1 et 4 !")

        elif choix == "5":
            sauvegarder_stock(fichier_produit, assignations)
            print("À bientôt !")
            enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Deconnexion")
            sys.exit()
        else:
            print("Option invalide. Veuillez choisir une option entre 0 et 5 !")
"""