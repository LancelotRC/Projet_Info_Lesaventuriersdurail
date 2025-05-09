from LesAventuriersDuRail import *


if __name__ == "__main__":
    print("\n=== Lancement manuel du jeu Les Aventuriers du Rail ===")

    # Création des joueurs
    joueurs = [Joueur("Alice", "rouge"), Joueur("Bob", "bleu"), Joueur("David", "Jaune")]
    table = Table(joueurs)

    
    #creation du plateau 
    plateau = Plateau(VILLES_USA,ROUTES_USA)
    plateau.routes[0].etat = "capturée"  # Marquer la première route comme capturée
    #L'état capturé fonctionne car la route[0] est en pointillé

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
    dernier_joueur = None
    dernier_tour = False
    while True:
        print(f"\n--- Tour {tour} ---")
        for joueur in joueurs:
            if dernier_tour and joueur == dernier_joueur:
                print(f"{joueur.nom} a déclenché la fin de partie au tour précédent.")
                print("Fin du jeu.")
                break  # On quitte la boucle for

            table.jouer_tour(joueur)

            if joueur.wagons_restants <=2 and not dernier_tour :
                dernier_joueur = joueur
                dernier_tour = True
                print(f"{joueur.nom} a {joueur.wagons_restants} wagons ou moins.")
                print("Dernier tour pour les autres joueurs.")
        else :
            tour += 1
            continue

        break
    Table.compte_des_points()
