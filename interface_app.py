from tkinter import *
import tkinter.messagebox as MessageBox
from log import verifier_connexion

def afficher_champs_saisie_connexion():
    boutonConnexion.pack_forget()
    boutonCreation.pack_forget()
    titre.pack_forget()

    label_email = Label(fenetre, text="E-mail utilisateur", font=("Arial", 10))
    label_email.pack(pady=5)
    value_email = StringVar()
    entree_email = Entry(fenetre, textvariable=value_email, width=30)
    entree_email.pack(pady=5)

    label_mdp = Label(fenetre, text="Mot de passe", font=("Arial", 10))
    label_mdp.pack(pady=5)
    value_mdp = StringVar()
    entree_mdp = Entry(fenetre, textvariable=value_mdp, width=30, show="*")
    entree_mdp.pack(pady=5)

    def confirmer_connexion():
        username = value_email.get().strip()
        password = value_mdp.get().strip()

        if not username or not password:
            MessageBox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        # Appel à la fonction de vérification de connexion
        success, user = verifier_connexion(username, password)
        if success:
            MessageBox.showinfo("Succès", f"Bienvenue {user}!")
            # Vous pouvez afficher l'écran principal ici après la connexion
        else:
            MessageBox.showerror("Erreur", "E-mail ou mot de passe invalide.")
    
    boutonConfirmer1 = Button(fenetre, text="Confirmer", command=confirmer_connexion, width=20, height=2, font=("Arial", 12))
    boutonConfirmer1.pack(pady=20)

from log import creer_compte

def afficher_champs_saisie_creation():
    boutonConnexion.pack_forget()
    boutonCreation.pack_forget()
    titre.pack_forget()

    label_email = Label(fenetre, text="E-mail utilisateur", font=("Arial", 10))
    label_email.pack(pady=5)
    value_email = StringVar()
    entree_email = Entry(fenetre, textvariable=value_email, width=30)
    entree_email.pack(pady=5)

    label_mdp = Label(fenetre, text="Mot de passe", font=("Arial", 10))
    label_mdp.pack(pady=5)
    value_mdp = StringVar()
    entree_mdp = Entry(fenetre, textvariable=value_mdp, width=30, show="*")
    entree_mdp.pack(pady=5)

    def confirmer_creation():
        username = value_email.get().strip()
        password = value_mdp.get().strip()

        if not username or not password:
            MessageBox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        # Appel à la fonction de création de compte
        success, user = creer_compte(username, password)
        if success:
            MessageBox.showinfo("Succès", f"Votre compte a été créé avec succès. Bienvenue {user}!")
            # Vous pouvez afficher l'écran principal ici après la création
        else:
            MessageBox.showerror("Erreur", "Ce compte existe déjà. Essayez un autre e-mail.")
    
    boutonConfirmer2 = Button(fenetre, text="Confirmer", command=confirmer_creation, width=20, height=2, font=("Arial", 12))
    boutonConfirmer2.pack(pady=20)

fenetre = Tk()
fenetre.geometry("800x500")
fenetre.title("Gestion de stock")

titre = Label(fenetre, text="Bienvenue sur l'application qui gère votre stock !", font=("Arial", 16))
titre.pack(pady=10)

boutonConnexion = Button(fenetre, text="Connexion", command=afficher_champs_saisie_connexion, width=20, height=3, font=("Arial", 14))
boutonConnexion.pack(pady=50)

boutonCreation = Button(fenetre, text="Créer un compte", command=afficher_champs_saisie_creation, width=20, height=3, font=("Arial", 14))
boutonCreation.pack(pady=50)

"""""
def user_menu():
    boutonCreation = Button(fenetre, text="Compte", command=afficher_compte, width=20, height=3, font=("Arial", 14))
    boutonCreation.pack(pady=50)
    boutonCreation = Button(fenetre, text="Afficher le stock", command=afficher_stock, width=20, height=3, font=("Arial", 14))
    boutonCreation.pack(pady=100)
"""""



fenetre.mainloop()
