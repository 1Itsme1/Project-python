fichier_stock = "stock.txt"

def lire_stock(fichier):
    stock = []
    with open(fichier, "r", encoding="utf-8") as f: 
        for ligne in f : 
            nom, prix, quantite = ligne.strip().split(",")
            stock.append({
                "nom": nom,
                "prix": float(prix),
                "stock": int(quantite) 
            })
    return stock

def afficher_stock(stock):
    print("{:<40} {:<10} {:<10}".format("Nom du produit", "Prix (€)", "Stock"))
    print("=" * 60)
    for produit in stock: 
        print("{:<40} {:<10} {:<10}".format(produit["nom"], produit["prix"], produit["stock"]))


if __name__ == "__main__":
    stock = lire_stock(fichier_stock)
    afficher_stock(stock)

