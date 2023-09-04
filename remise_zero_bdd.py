import os


# Réinitialise la base de données json au lancement du programme
# Environnement de developpement seulement
def remise_zero_bdd():
    # Remise à zéro base de données clubs
    if os.path.exists("clubs.json"):
        with open("original_clubs.json", "r") as fichier:
            data = fichier.read()
        with open("clubs.json", "w") as fichier:
            fichier.write(data)

    # Remise à zéro base de données competitions
    if os.path.exists("competitions.json"):
        with open("original_competitions.json", "r") as fichier:
            data = fichier.read()
        with open("competitions.json", "w") as fichier:
            fichier.write(data)

    # Remise à zéro base de données historique de reservation
    if os.path.exists("historique_reservation.json"):
        with open("original_historique_reservation.json", "r") as fichier:
            data = fichier.read()
        with open("historique_reservation.json", "w") as fichier:
            fichier.write(data)
