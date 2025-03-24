from LesAventuriersDuRail import *

if __name__ == "__main__":
    print("\n=== Lancement manuel du jeu Les Aventuriers du Rail ===")

    # Création des joueurs
    joueurs = [Joueur("Alice", "rouge"), Joueur("Bob", "bleu")]
    table = Table(joueurs)

    # Initialisation de la partie
    print("\n=== Initialisation de la partie ===")
    table.initialiser_partie()

    # Afficher les cartes de départ des joueurs
    for joueur in joueurs:
        print(f"\n{joueur.nom} ({joueur.couleur}) commence avec :")
        print("Cartes wagon :", [c.couleur for c in joueur.cartes_wagon])
        print("Cartes destination :", [f"{c.ville_depart} → {c.ville_arrivee}" for c in joueur.cartes_defi])

    # Début de la partie (chaque joueur joue à tour de rôle)
    print("\n=== Début de la partie ===")
    tour = 1
    while True:
        print(f"\n--- Tour {tour} ---")
        for joueur in joueurs:
            print(f"\n{joueur.nom}, c'est votre tour !")
            print("1. Piocher une carte wagon")
            print("2. Capturer une route")
            print("3. Piocher des cartes destination")
            print("4. Quitter le jeu")
            choix = input("Choisissez une action (1, 2, 3, 4) : ")

            if choix == "1":
                table.piocher_cartes_wagon(joueur)
            elif choix == "2":
                table.capturer_route(joueur)
            elif choix == "3":
                table.piocher_cartes_itineraire(joueur)
            elif choix == "4":
                print("Fin de la partie. Merci d'avoir joué !")
                exit()
            else:
                print("Choix invalide, veuillez réessayer.")

        tour += 1
