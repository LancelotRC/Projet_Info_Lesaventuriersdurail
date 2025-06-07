from LesAventuriersDuRail import *

if __name__ == "__main__":
    print("\n=== Lancement manuel du jeu Les Aventuriers du Rail ===")

    # Création des joueurs
    joueurs = [Joueur("Alice", "red"), JoueurAuto("Bob", "blue"), JoueurAuto("David", "pink")]
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
        print("Cartes destination :", [f"{c.ville_depart.nom} → {c.ville_arrivee.nom}" for c in joueur.cartes_defi])

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

            if isinstance(joueur, JoueurAuto):
                print(f"{joueur.nom} est un joueur automatique.")
                joueur.jouer_automatiquement(table)
            else:
                print(f"{joueur.nom} n'est pas un joueur automatique.")
                table.jouer_tour(joueur)

            if joueur.wagons_restants <=2 and not dernier_tour :
                dernier_joueur = joueur
                dernier_tour = True
                print(f"{joueur.nom} a {joueur.wagons_restants} wagons ou moins.")
                print("Dernier tour pour les autres joueurs.")
        else :
            for joueur in table.joueurs:
                print(f"\n=== Résumé pour {joueur.nom} ===")
                print("Routes capturées :")
                for route in joueur.routes_capturees:
                    print(f"- {route.Ville1.nom} → {route.Ville2.nom} ({route.longueur} cases, {route.couleur})")
                #joueur.afficher_son_graphe()
                table.afficher_routes_disponibles()

            tour += 1
            continue
        if dernier_tour :
            break

    table.plateau.afficher_plateau_graphique()
    table.compte_des_points()
