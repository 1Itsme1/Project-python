import csv
from hashlib import sha256
import os
import base64
from Main import verifier_password
from Main import lire_stock_global

def generer_salt():
    return base64.b64encode(os.urandom(16)).decode('utf-8')

def verifier_connexion(email, password):
    fichier_usernames_passwords = "./Data/usernames_passwords.csv"
    
    if not os.path.exists(fichier_usernames_passwords):
        return False, None  
    
    with open(fichier_usernames_passwords, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        rows = list(reader)

    hash_user = sha256(email.encode('utf-8')).hexdigest()

    for row in rows[1:]:
        if len(row) < 3:
            continue
        log_user, salt, log_password = row
        if log_user.strip() == hash_user:
            hash_password = sha256((salt + password).encode('utf-8')).hexdigest()
            if hash_password == log_password.strip():
                return True, email
    
    return False, None

def creer_compte(email, password):
    fichier_usernames_passwords = "./Data/usernames_passwords.csv"
    
    if not os.path.exists(fichier_usernames_passwords):
        with open(fichier_usernames_passwords, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["hash_utilisateur", "salt", "hash_mot_de_passe"])

    with open(fichier_usernames_passwords, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        rows = list(reader)

    
    hash_user = sha256(email.encode('utf-8')).hexdigest()
    for row in rows[1:]:
        if len(row) < 3:
            continue
        log_user = row[0].strip()
        if log_user == hash_user:
            return False, None

    
    salt = generer_salt()
    hash_password = sha256((salt + password).encode('utf-8')).hexdigest()

    with open(fichier_usernames_passwords, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([hash_user, salt, hash_password])

    return True, email
