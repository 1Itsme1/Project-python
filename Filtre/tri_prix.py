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


def tri_prix_stock (stock):
    n = len(stock)
    for i in range (n): 
        for j in range(0, n-i-1):
            if stock[j]["prix"] > stock[j+1]["prix"]:
                stock[j], stock[j+1] = stock[j+1], stock[j]               
    return stock


if __name__ == "__main__":
    stock = lire_stock(fichier_stock)
    tri_prix_stock(stock)
    afficher_stock(stock)
    
    