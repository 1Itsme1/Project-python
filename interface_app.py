from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as MessageBox
from log import verifier_connexion, creer_compte
from Main import lire_stock_global_all,verifier_mot_de_passe,suppression_compte,changer_mot_de_passe_graphique, lire_stock_global, sauvegarder_stock, enregistrer_historique_requete,verifier_password
from hashlib import sha256
import json
import customtkinter as ctk
from datetime import datetime
#===========================================================================================================
def afficher_page_connexion():
    
    for widget in fenetre.winfo_children():
        widget.pack_forget()

    
    titre.pack(pady=30)
    boutonConnexion.pack(pady=20, fill=X, padx=50)
    boutonCreation.pack(pady=20, fill=X, padx=50)
#===========================================================================================================

def afficher_champs_saisie_connexion():
    
    boutonConnexion.pack_forget()
    boutonCreation.pack_forget()
    titre.pack_forget()

    
    frame_connexion = Frame(fenetre, padx=30, pady=30)
    frame_connexion.pack(pady=20)

   
    label_email = Label(frame_connexion, text="E-mail utilisateur", font=("Helvetica", 12), anchor="w")
    label_email.pack(fill=X, pady=5)
    value_email = StringVar()
    entree_email = Entry(frame_connexion, textvariable=value_email, width=30, font=("Helvetica", 12), bd=2)
    entree_email.pack(pady=10)

    label_mdp = Label(frame_connexion, text="Mot de passe", font=("Helvetica", 12), anchor="w")
    label_mdp.pack(fill=X, pady=5)
    value_mdp = StringVar()
    entree_mdp = Entry(frame_connexion, textvariable=value_mdp, width=30, font=("Helvetica", 12), bd=2, show="*")
    entree_mdp.pack(pady=10)

    def confirmer_connexion():
        username = value_email.get().strip()
        password = value_mdp.get().strip()

        if not username or not password:
            MessageBox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        
        success, user = verifier_connexion(username, password)
        if success:
            verifier_password(password,username)
            MessageBox.showinfo("Succès", f"Bienvenue {user}!")
            utilisateur_hash = sha256(username.strip().encode('utf-8')).hexdigest()
            enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"Connexion au compte de {username}")
            afficher_page_principale(user)
        else:
            MessageBox.showerror("Erreur", "E-mail ou mot de passe invalide.")

    boutonConfirmer1 = Button(frame_connexion, text="Confirmer", command=confirmer_connexion, width=20, height=2, font=("Helvetica", 12), bg="#28A745", fg="white", bd=0)
    boutonConfirmer1.pack(pady=20)

    boutonRetour = Button(frame_connexion, text="Retour", command=afficher_page_connexion, width=15, height=2, font=("Helvetica", 12), bg="#DC3545", fg="white", bd=0)
    boutonRetour.pack(pady=10)
#===========================================================================================================

def afficher_champs_saisie_creation():
    boutonConnexion.pack_forget()
    boutonCreation.pack_forget()
    titre.pack_forget()

    frame_creation = Frame(fenetre, padx=30, pady=30)
    frame_creation.pack(pady=20)

    label_email = Label(frame_creation, text="E-mail utilisateur", font=("Helvetica", 12), anchor="w")
    label_email.pack(fill=X, pady=5)
    value_email = StringVar()
    entree_email = Entry(frame_creation, textvariable=value_email, width=30, font=("Helvetica", 12), bd=2)
    entree_email.pack(pady=10)

    label_mdp = Label(frame_creation, text="Mot de passe", font=("Helvetica", 12), anchor="w")
    label_mdp.pack(fill=X, pady=5)
    value_mdp = StringVar()
    entree_mdp = Entry(frame_creation, textvariable=value_mdp, width=30, font=("Helvetica", 12), bd=2, show="*")
    entree_mdp.pack(pady=10)

    def confirmer_creation():
        username = value_email.get().strip()
        password = value_mdp.get().strip()

        if not username or not password:
            MessageBox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        
        success, user = creer_compte(username, password)
        if success:
            name_avant_arobase = user.split('@')[0]
            MessageBox.showinfo("Succès", f"Votre compte a été créé avec succès. Bienvenue {name_avant_arobase}!")
            enregistrer_historique_requete("./Data/historique_requetes.csv", username, f"Création du compte {username}...")
            afficher_page_connexion() 
        else:
            MessageBox.showerror("Erreur", "Ce compte existe déjà. Essayez un autre e-mail.")

    boutonConfirmer2 = Button(frame_creation, text="Confirmer", command=confirmer_creation, width=20, height=2, font=("Helvetica", 12), bg="#28A745", fg="white", bd=0)
    boutonConfirmer2.pack(pady=20)

    boutonRetour = Button(frame_creation, text="Retour", command=afficher_page_connexion, width=15, height=2, font=("Helvetica", 12), bg="#DC3545", fg="white", bd=0)
    boutonRetour.pack(pady=10)
#===========================================================================================================

def afficher_page_principale(utilisateur):
    
    for widget in fenetre.winfo_children():
        try:
            widget.pack_forget()
        except Exception as e:
            print(f"Erreur lors de l'oubli du widget {widget}: {e}")

    name_avant_arobase = utilisateur.split('@')[0]
    titre_principal = Label(fenetre, text=f"Bienvenue {name_avant_arobase} !", font=("Helvetica", 16))
    titre_principal.pack(pady=30)

    bouton_compte = Button(fenetre, text="Compte", width=20, height=3, font=("Helvetica", 14), bg="#28A745", fg="white", bd=0,command=lambda: afficher_page_compte(utilisateur))
    bouton_compte.pack(pady=10)

    bouton_afficher_stock = Button(fenetre, text="Mon stock", width=20, height=3, font=("Helvetica", 14), bg="#2196F3", fg="white", bd=0, command=lambda: afficher_stock(utilisateur))
    bouton_afficher_stock.pack(pady=10)

    bouton_commandes = Button(fenetre, text="Commander", width=20,command=lambda: affichage_commander(utilisateur), height=3, font=("Helvetica", 14), bg="#F39C12", fg="white", bd=0)
    bouton_commandes.pack(pady=10)

    bouton_liste_commandes = Button(fenetre, text="Liste des commandes", width=20, height=3, font=("Helvetica", 14), bg="#F39C12", fg="white", bd=0)
    bouton_liste_commandes.pack(pady=10)


    bouton_deconnexion = Button(fenetre, text="Déconnexion", command=lambda:deconnexion(utilisateur), width=20, height=3, font=("Helvetica", 14), bg="#DC3545", fg="white", bd=0)
    bouton_deconnexion.pack(pady=10)

    bouton_quitter = Button(fenetre, text="Quitter", command=lambda: quitter_fenetre(utilisateur), width=20, height=3, font=("Helvetica", 14), bg="#DC3545", fg="white", bd=0)
    bouton_quitter.pack(pady=10)
#===========================================================================================================
def quitter_fenetre(utilisateur):
    fenetre.quit()
    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur, f"A quitter l'application")

def afficher_stock_gui(fenetre, assignations, utilisateur_hash):
    tree = ttk.Treeview(fenetre, columns=("Nom", "Prix (€)", "Stock"), show="headings")
    tree.heading("Nom", text="Nom du produit")
    tree.heading("Prix (€)", text="Prix (€)")
    tree.heading("Stock", text="Stock")


    if utilisateur_hash in assignations:
        produits = assignations[utilisateur_hash]
        for produit in produits:
            tree.insert("", "end", values=(produit["nom"], produit["prix"], produit["stock"]))
    else:
        tree.insert("", "end", values=("Aucun produit", "", ""))

    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    return tree
#========================================================
def afficher_stock_gui_all(fenetre, assignations): 
    tree = ttk.Treeview(fenetre, columns=("Nom", "Prix (€)", "Stock"), show="headings")
    
    tree.heading("Nom", text="Nom du produit")
    tree.heading("Prix (€)", text="Prix (€)")
    tree.heading("Stock", text="Stock")
    

    # Ajouter les produits au tableau
    for produit in assignations:
        tree.insert("", "end", values=(produit["nom"], produit["prix"], produit["stock"]))
    
    tree.pack(fill="both", expand=True)
    return tree

#===========================================================================================================
def afficher_stock(utilisateur):
    for widget in fenetre.winfo_children():
        widget.pack_forget()

    
    assignations = lire_stock_global(fichier_produit, utilisateur)
    utilisateur_hash = sha256(utilisateur.strip().encode('utf-8')).hexdigest()
    enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur, f"Affichage du stock")

    def tri_rapide(stock, key, reverse=False):
        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"Tri du stock")
        return sorted(stock, key=lambda x: x[key], reverse=reverse)


    def rafraichir_treeview(produits):

        for item in tree.get_children():
            tree.delete(item)


        for produit in produits:
            tree.insert("", "end", values=(produit["nom"], produit["prix"], produit["stock"]))


    frame_outils = Frame(fenetre, padx=10, pady=10)
    frame_outils.pack()


    Label(frame_outils, text="Rechercher un produit : ", font=("Helvetica", 12)).pack(side=LEFT, padx=5)
    valeur_recherche = StringVar()
    entry_recherche = Entry(frame_outils, textvariable=valeur_recherche, font=("Helvetica", 12), width=30)
    entry_recherche.pack(side=LEFT, padx=5)

    def rechercher_produit():
        nom_recherche = valeur_recherche.get().strip().lower()
        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"Recherche produits")
        if not nom_recherche:
            MessageBox.showerror("Erreur", "Veuillez entrer un nom de produit à rechercher.")
            return

        produits_trouves = []
        if utilisateur_hash in assignations:
            for produit in assignations[utilisateur_hash]:
                if nom_recherche in produit["nom"].lower():
                    produits_trouves.append(produit)

        if produits_trouves:
            enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"prdouit {nom_recherche} trouver")
            rafraichir_treeview(produits_trouves)
        else:
            enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"prdouit {nom_recherche} introuvable")
            MessageBox.showinfo("Aucun résultat", "Aucun produit trouvé avec ce nom.")

    Button(frame_outils, text="Rechercher", command=rechercher_produit, font=("Helvetica", 12), bg="#6C757D", fg="white").pack(side=LEFT, padx=5)

   
    Label(frame_outils, text="Trier par : ", font=("Helvetica", 12)).pack(side=LEFT, padx=10)

    Button(frame_outils, text="Nom", command=lambda: trier_stock("nom"), font=("Helvetica", 12), bg="#007BFF", fg="white").pack(side=LEFT, padx=5)
    Button(frame_outils, text="Prix", command=lambda: trier_stock("prix"), font=("Helvetica", 12), bg="#007BFF", fg="white").pack(side=LEFT, padx=5)
    Button(frame_outils, text="Quantité", command=lambda: trier_stock("stock"), font=("Helvetica", 12), bg="#007BFF", fg="white").pack(side=LEFT, padx=5)


    def trier_stock(critere):
        produits = assignations.get(utilisateur_hash, [])
        produits_tries = tri_rapide(produits, key=critere)
        rafraichir_treeview(produits_tries)


    tree = afficher_stock_gui(fenetre, assignations, utilisateur_hash)


    Button(fenetre, text="Ajouter un produit", command=lambda: ajouter_produit_gui(fenetre, assignations, utilisateur_hash, tree), width=20, height=2, font=("Helvetica", 12), bg="#28A745", fg="white", bd=0).pack(pady=10)
    Button(fenetre, text="Modifier un produit", command=lambda: modifier_produit_gui(fenetre, assignations, utilisateur_hash, tree), width=20, height=2, font=("Helvetica", 12), bg="#FFC107", fg="white", bd=0).pack(pady=10)
    Button(fenetre, text="Supprimer un produit", command=lambda: supprimer_produit_gui(fenetre, assignations, utilisateur_hash, tree), width=20, height=2, font=("Helvetica", 12), bg="#DC3545", fg="white", bd=0).pack(pady=10)
    
    bouton_retour = Button(fenetre, text="Retour", command=lambda: afficher_page_principale(utilisateur), width=20, height=2, font=("Helvetica", 12), bg="#6C757D", fg="white", bd=0)
    bouton_retour.pack(pady=20)



#===========================================================================================================

def ajouter_produit_gui(fenetre, assignations, utilisateur_hash, tree):
    def ajouter():
        nom = entry_nom.get()
        try:
            prix = float(entry_prix.get())
            quantite = int(entry_quantite.get())
        except ValueError:
            MessageBox.showerror("Erreur", "Le prix et la quantité doivent être des valeurs valides.")
            return
        
        if utilisateur_hash not in assignations:
            assignations[utilisateur_hash] = []
        
        assignations[utilisateur_hash].append({"nom": nom, "prix": prix, "stock": quantite})
        sauvegarder_stock(fichier_produit, assignations)
        tree.insert("", "end", values=(nom, prix, quantite))
        MessageBox.showinfo("Succès", f"Produit '{nom}' ajouté avec succès !")
        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"Ajout du porduit {nom}")
        ajouter_window.destroy()

    ajouter_window = Toplevel(fenetre)
    ajouter_window.title("Ajouter un produit")

    Label(ajouter_window, text="Nom du produit").pack(pady=5)
    entry_nom = Entry(ajouter_window)
    entry_nom.pack(pady=5)

    Label(ajouter_window, text="Prix (€)").pack(pady=5)
    entry_prix = Entry(ajouter_window)
    entry_prix.pack(pady=5)

    Label(ajouter_window, text="Quantité").pack(pady=5)
    entry_quantite = Entry(ajouter_window)
    entry_quantite.pack(pady=5)

    Button(ajouter_window, text="Ajouter", command=ajouter).pack(pady=20)
    Button(ajouter_window, text="Annuler", command=ajouter_window.destroy).pack(pady=5)

#===========================================================================================================
def modifier_produit_gui(fenetre, assignations, utilisateur_hash, tree):
    def modifier():
        selected_item = tree.selection()
        if not selected_item:
            MessageBox.showerror("Erreur", "Veuillez sélectionner un produit à modifier.")
            return
        
        produit = tree.item(selected_item)["values"]
        nom = produit[0]
        
        for p in assignations[utilisateur_hash]:
            if p["nom"] == nom:

                choix_modification = Toplevel(fenetre)
                choix_modification.title(f"Modifier le produit {nom}")
                
                label_choix = Label(choix_modification, text="Que voulez-vous modifier ?")
                label_choix.pack(pady=10)
                
                def modifier_nom():
                    nouveau_nom = entry_nouveau_nom.get()
                    if nouveau_nom:
                        p["nom"] = nouveau_nom
                        tree.item(selected_item, values=(nouveau_nom, p["prix"], p["stock"]))
                        sauvegarder_stock(fichier_produit, assignations)
                        MessageBox.showinfo("Succès", f"Nom modifié en '{nouveau_nom}'")
                        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"Modification nom du produit {nom} en {nouveau_nom} ")   
                    else:
                        MessageBox.showerror("Erreur", "Le nouveau nom ne peut pas être vide.")
                    choix_modification.destroy()
                
                def modifier_prix():
                    try:
                        nouveau_prix = float(entry_nouveau_prix.get())
                        p["prix"] = nouveau_prix
                        tree.item(selected_item, values=(p["nom"], nouveau_prix, p["stock"]))
                        sauvegarder_stock(fichier_produit, assignations)
                        MessageBox.showinfo("Succès", f"Prix modifié en '{nouveau_prix} €'")
                        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"Modification du prix de {nom} à {nouveau_prix}")                       
                    except ValueError:
                        MessageBox.showerror("Erreur", "Le prix doit être un nombre valide.")
                    choix_modification.destroy()

                def modifier_quantite():
                    try:
                        nouvelle_quantite = int(entry_nouvelle_quantite.get())
                        p["stock"] = nouvelle_quantite
                        tree.item(selected_item, values=(p["nom"], p["prix"], nouvelle_quantite))
                        sauvegarder_stock(fichier_produit, assignations)
                        MessageBox.showinfo("Succès", f"Quantité modifiée à {nouvelle_quantite}")
                        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"Modification de la quantité de {nom} à {nouvelle_quantite}")
                    except ValueError:
                        MessageBox.showerror("Erreur", "La quantité doit être un nombre entier valide.")
                    choix_modification.destroy()
                

                bouton_nom = Button(choix_modification, text="Modifier le nom", command=lambda: modifier_nom())
                bouton_nom.pack(pady=10)
                
                bouton_prix = Button(choix_modification, text="Modifier le prix", command=lambda: modifier_prix())
                bouton_prix.pack(pady=10)
                
                bouton_quantite = Button(choix_modification, text="Modifier la quantité", command=lambda: modifier_quantite())
                bouton_quantite.pack(pady=10)
                

                Label(choix_modification, text="Nouveau nom :").pack(pady=5)
                entry_nouveau_nom = Entry(choix_modification)
                entry_nouveau_nom.pack(pady=5)
                
                Label(choix_modification, text="Nouveau prix :").pack(pady=5)
                entry_nouveau_prix = Entry(choix_modification)
                entry_nouveau_prix.pack(pady=5)
                
                Label(choix_modification, text="Nouvelle quantité :").pack(pady=5)
                entry_nouvelle_quantite = Entry(choix_modification)
                entry_nouvelle_quantite.pack(pady=5)

    modifier_window = Toplevel(fenetre)
    modifier_window.title("Modifier un produit")
    Button(modifier_window, text="Modifier le produit", command=modifier).pack(pady=20)

#===========================================================================================================
def supprimer_produit_gui(fenetre, assignations, utilisateur_hash, tree):
    def supprimer():
        selected_items = tree.selection()
        if not selected_items:
            MessageBox.showerror("Erreur", "Veuillez sélectionner un ou plusieurs produits à supprimer.")
            return
        
        for selected_item in selected_items:
            produit = tree.item(selected_item)["values"]
            nom = produit[0]


            for p in assignations[utilisateur_hash]:
                if p["nom"] == nom:
                    assignations[utilisateur_hash].remove(p)
                    break
            tree.delete(selected_item)
        sauvegarder_stock(fichier_produit, assignations)
        MessageBox.showinfo("Succès", f"{len(selected_items)} produit(s) supprimé(s) avec succès !")
        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"{selected_item} produits supprimer : {nom}")
        supprimer_window.destroy()


    supprimer_window = Toplevel(fenetre)
    supprimer_window.title("Supprimer un ou plusieurs produits")
    Button(supprimer_window, text="Supprimer le(s) produit(s)", command=supprimer).pack(pady=20)

#===========================================================================================================
def afficher_page_compte(utilisateur):
    name_avant_arobase = utilisateur.split('@')[0]
    utilisateur_hash = sha256(utilisateur.strip().encode('utf-8')).hexdigest()

    for widget in fenetre.winfo_children():
        widget.pack_forget()

    titre_compte = Label(fenetre, text="Gestion du compte", font=("Helvetica", 16))
    titre_compte.pack(pady=30)
    titre_principal = Label(fenetre, text=f"Compte de {name_avant_arobase} ", font=("Helvetica", 16))
    titre_principal.pack(pady=30)

    bouton_changer_mdp = Button(fenetre, text="Changer mon mot de passe", 
                                 command=lambda: changer_mot_de_passe_graphique(fichier_usernames_passwords,utilisateur_hash,fenetre), 
                                 width=20, height=2, font=("Helvetica", 12), bg="#007BFF", fg="white", bd=0)
    bouton_changer_mdp.pack(pady=10)

    bouton_supp_compte = Button(fenetre, text="Supprimer mon compte",  
                             command=lambda: suppression_compte(fichier_usernames_passwords, fichier_produit, utilisateur_hash, verifier_mot_de_passe, fenetre), 
                             width=20, height=2, font=("Helvetica", 12), bg="#DC3545", fg="white", bd=0)
    bouton_supp_compte.pack(pady=10)


    bouton_retour = Button(fenetre, text="Retour", command=lambda: afficher_page_principale(utilisateur), 
                           width=20, height=2, font=("Helvetica", 12), bg="#6C757D", fg="white", bd=0)
    bouton_retour.pack(pady=10)

#===========================================================================================================
def affichage_commander(utilisateur):
   
    for widget in fenetre.winfo_children():
        widget.pack_forget()

    def tri_rapide(stock, key, reverse=False):
        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, f"Tri du stock pour commander")
        return sorted(stock, key=lambda x: x[key], reverse=reverse)
    
    utilisateur_hash = sha256(utilisateur.strip().encode('utf-8')).hexdigest()
    assignations = lire_stock_global_all(fichier_produit) 

    
    Label(fenetre, text="Liste des produits disponibles", font=("Helvetica", 16)).pack(pady=20)

    
    tree = afficher_stock_gui_all(fenetre, assignations)
    
    frame_outils = Frame(fenetre, padx=10, pady=10)
    frame_outils.pack()

    
    def rafraichir_treeview(produits):
        for item in tree.get_children():
            tree.delete(item)
        for produit in produits:
            tree.insert("", "end", values=(produit["nom"], produit["prix"], produit["stock"]))

    
    def rechercher_produit():
        nom_recherche = valeur_recherche.get().strip().lower()
        if not nom_recherche:
            MessageBox.showerror("Erreur", "Veuillez entrer un nom de produit à rechercher.")
            return

        produits_trouves = [produit for produit in assignations if nom_recherche in produit["nom"].lower()]

        if produits_trouves:
            rafraichir_treeview(produits_trouves)
        else:
            MessageBox.showinfo("Aucun résultat", "Aucun produit trouvé avec ce nom.")

    
    def trier_stock(critere):
        produits_tries = tri_rapide(assignations, key=critere)
        rafraichir_treeview(produits_tries)

   
    Label(frame_outils, text="Rechercher un produit : ", font=("Helvetica", 12)).pack(side=LEFT, padx=5)
    valeur_recherche = StringVar()
    entry_recherche = Entry(frame_outils, textvariable=valeur_recherche, font=("Helvetica", 12), width=30)
    entry_recherche.pack(side=LEFT, padx=5)

    Button(frame_outils, text="Rechercher", command=rechercher_produit, font=("Helvetica", 12), bg="#6C757D", fg="white").pack(side=LEFT, padx=5)

    
    Label(frame_outils, text="Trier par : ", font=("Helvetica", 12)).pack(side=LEFT, padx=10)
    Button(frame_outils, text="Nom", command=lambda: trier_stock("nom"), font=("Helvetica", 12), bg="#007BFF", fg="white").pack(side=LEFT, padx=5)
    Button(frame_outils, text="Prix", command=lambda: trier_stock("prix"), font=("Helvetica", 12), bg="#007BFF", fg="white").pack(side=LEFT, padx=5)
    Button(frame_outils, text="Quantité", command=lambda: trier_stock("stock"), font=("Helvetica", 12), bg="#007BFF", fg="white").pack(side=LEFT, padx=5)

    Label(fenetre, text="Quantité à commander :", font=("Helvetica", 12)).pack(pady=10)
    quantite_var = StringVar()
    Entry(fenetre, textvariable=quantite_var, font=("Helvetica", 12)).pack(pady=10)

    
    commandes = []
#=======================================
    def ajouter_au_panier():
        selected_items = tree.selection()
        if not selected_items:
            MessageBox.showerror("Erreur", "Veuillez sélectionner un produit.")
            return

        for item in selected_items:
            produit = tree.item(item)["values"]
            try:
                quantite = int(quantite_var.get())
                if quantite <= 0:
                    raise ValueError
            except ValueError:
                MessageBox.showerror("Erreur", "Veuillez entrer une quantité valide.")
                return

            commandes.append({
                "nom": produit[0],
                "prix_unitaire": produit[1],
                "quantite": quantite,
                "prix_total": produit[1] * quantite
            })
            MessageBox.showinfo("Succès", f"Produit '{produit[0]}' ajouté au panier.")

        quantite_var.set("")
#=======================================
    def finaliser_commande():
        if not commandes:
            MessageBox.showerror("Erreur", "Le panier est vide.")
            return
        try:
            with open(fichier_commandes, "r") as f:
                historique_commandes = json.load(f)
        except FileNotFoundError:
            historique_commandes = []

        commande = {
            "utilisateur": utilisateur_hash,
            "produits": commandes,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        historique_commandes.append(commande)

        with open(fichier_commandes, "w") as f:
            json.dump(historique_commandes, f, indent=4)

        MessageBox.showinfo("Succès", "Commande enregistrée avec succès !")
        enregistrer_historique_requete("./Data/historique_requetes.csv", utilisateur_hash, "Nouvelle commande enregistrée")
        afficher_page_principale(utilisateur)

    Button(fenetre, text="Ajouter au panier", command=ajouter_au_panier, font=("Helvetica", 12), bg="#28A745", fg="white").pack(pady=10)
    Button(fenetre, text="Finaliser la commande", command=finaliser_commande, font=("Helvetica", 12), bg="#007BFF", fg="white").pack(pady=10)
    Button(fenetre, text="Retour", command=lambda: afficher_page_principale(utilisateur), font=("Helvetica", 12), bg="#6C757D", fg="white").pack(pady=20)              
#===========================================================================================================
def deconnexion(utilisateur):
    MessageBox.showinfo("Déconnexion", "Vous êtes maintenant déconnecté.")
    enregistrer_historique_requete("./Data/historique_requetes.csv",utilisateur, "Déconnexion...")
    afficher_page_connexion()
#===========================================================================================================

fenetre = Tk()  
fenetre.geometry("1200x900")
fenetre.title("Gestion de stock")
fenetre.config(bg="#F8F9FA")  


titre = Label(fenetre, text="Bienvenue sur l'application qui gère votre stock !", font=("Helvetica", 18, "bold"), fg="#343A40")
titre.pack(pady=30)


boutonConnexion = Button(fenetre, text="Connexion", command=afficher_champs_saisie_connexion, width=20, height=3, font=("Helvetica", 14), bg="#28A745", fg="white", bd=0)
boutonConnexion.pack(pady=20, fill=X, padx=50)

boutonCreation = Button(fenetre, text="Créer un compte", command=afficher_champs_saisie_creation, width=20, height=3, font=("Helvetica", 14), bg="#28A745", fg="white", bd=0)
boutonCreation.pack(pady=20, fill=X, padx=50)

fichier_commandes = "./DATA/commandes.json"
fichier_produit = "./Data/assignations_stock.csv"
fichier_usernames_passwords = "./Data/usernames_passwords.csv"
fenetre.mainloop()
