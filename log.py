import csv
from hashlib import sha256
from getpass import getpass

def account():
        with open('usernames_passwords.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rows = list(reader)
        
        print("--------------------------------------------")
        log = input("Bonjour, avez-vous un compte ? Oui/Non : ").strip().lower()
        print("--------------------------------------------")
        
        if log == "oui":
            user = input("Nom d'utilisateur: ").strip()
            user_entrer = sha256(user.encode('utf-8')).hexdigest()
            password = getpass("Mot de passe: ").strip()
            hash_user = sha256(user.encode('utf-8')).hexdigest()
            hash_password = sha256(password.encode('utf-8')).hexdigest()

            for row in rows[1:]: 
                if len(row) < 2:  
                    continue
                log_user = row[0].strip()
                log_password = row[1].strip()
                if log_user == hash_user and log_password == hash_password:
                    return True, user     
            return False, None  

        elif log == "non":
            user = input("Choisissez un nom d'utilisateur: ").strip()
            password = getpass("Choisissez un mot de passe: ").strip()

            for row in rows[1:]:  
                if len(row) < 2:  
                    continue
                log_user = row[0].strip()
                if log_user == user:
                    print("Ce nom d'utilisateur existe déjà. Essayez un autre.")
                    return False, None

            hash_user = sha256(user.encode('utf-8')).hexdigest()
            hash_password = sha256(password.encode('utf-8')).hexdigest()

            with open('usernames_passwords.csv', 'a', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([hash_user, hash_password])
                print(f"Votre compte a été créé avec succès. Bienvenue {user} !")
            return True, user 
        
        else:
            print("Réponse invalide. Veuillez répondre par Oui ou Non.")
            return False, None

if __name__ == "__main__":
    check, user = account()

    if check:
        print(f"Bienvenu {user} !")
    else:
        print("Nom d'utilisateur ou mot de passe invalide.")
