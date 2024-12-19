import csv
from hashlib import sha256
from getpass import getpass
import os
import base64


def generer_salt():
    """Génère un sel aléatoire sous forme de chaîne base64."""
    return base64.b64encode(os.urandom(16)).decode('utf-8')


def account():
    
    if not os.path.exists('usernames_passwords.csv'):
        with open('usernames_passwords.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["hash_utilisateur", "salt", "hash_mot_de_passe"])
    
    with open('usernames_passwords.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        rows = list(reader)
    
    print("--------------------------------------------")
    log = input("Bonjour, avez-vous un compte ? Oui/Non : ").strip().lower()
    print("--------------------------------------------")
    
    if log == "oui":
       
        user = input("Nom d'utilisateur: ").strip()
        password = getpass("Mot de passe: ").strip()
        hash_user = sha256(user.encode('utf-8')).hexdigest()

        for row in rows[1:]:  
            if len(row) < 3: 
                continue
            log_user, salt, log_password = row
            if log_user.strip() == hash_user:
                
                hash_password = sha256((salt + password).encode('utf-8')).hexdigest()
                if hash_password == log_password.strip():
                    return True, user  
        print("Nom d'utilisateur ou mot de passe invalide.")
        return False, None

    elif log == "non":
       
        user = input("Choisissez un nom d'utilisateur: ").strip()
        password = getpass("Choisissez un mot de passe: ").strip()

       
        for row in rows[1:]:  
            if len(row) < 3:  
                continue
            log_user = row[0].strip()
            if log_user == sha256(user.encode('utf-8')).hexdigest():
                print("Ce nom d'utilisateur existe déjà. Essayez un autre.")
                return False, None

        
        salt = generer_salt()
        hash_user = sha256(user.encode('utf-8')).hexdigest()
        hash_password = sha256((salt + password).encode('utf-8')).hexdigest()

       
        with open('usernames_passwords.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([hash_user, salt, hash_password])
            print(f"Votre compte a été créé avec succès. Bienvenue {user} !")
        return True, user
    
    else:
        print("Réponse invalide. Veuillez répondre par Oui ou Non.")
        return False, None


if __name__ == "__main__":
    check, user = account()

    if check:
        print(f"Bienvenue {user} !")
    else:
        print("Nom d'utilisateur ou mot de passe invalide.")
