def remplacer_hash(fichier_csv, hash_source, hash_cible):
    try:
        with open(fichier_csv, "r", encoding="utf-8") as f:
            lignes = f.readlines()

        lignes_modifiees = [
            ligne.replace(hash_source, hash_cible) for ligne in lignes
        ]

        with open(fichier_csv, "w", encoding="utf-8") as f:
            f.writelines(lignes_modifiees)

        print(f"Le hash '{hash_source}' a été remplacé par '{hash_cible}' dans '{fichier_csv}'.")
    except FileNotFoundError:
        print(f"Fichier '{fichier_csv}' introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

# Exemple d'utilisation :
fichier_csv = "assignations_stock.csv"
hash_source = "b822f99a7142e909d1b0df5b7f73270e083a1900bc11003d8e4dfcf5f53f7f5e"
hash_cible = "6025d18fe48abd45168528f18a82e265dd98d421a7084aa09f61b341703901a3"
remplacer_hash(fichier_csv, hash_source, hash_cible)
