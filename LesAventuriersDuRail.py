#region === Imports ===

import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from collections import Counter

#endregion

#region === definition des données pour le jeu version USA ===

# Définition des villes du plateau USA
VILLES_USA = {
    "Atlanta": (0.62, 0.35),
    "Boston": (0.88, 0.80),
    "Calgary": (0.15, 0.95),
    "Charleston": (0.70, 0.30),
    "Chicago": (0.60, 0.60),
    "Dallas": (0.48, 0.32),
    "Denver": (0.35, 0.55),
    "Duluth": (0.55, 0.70),
    "El Paso": (0.28, 0.28),
    "Helena": (0.28, 0.75),
    "Houston": (0.50, 0.25),
    "Kansas City": (0.48, 0.48),
    "Las Vegas": (0.20, 0.45),
    "Little Rock": (0.52, 0.38),
    "Los Angeles": (0.15, 0.25),
    "Miami": (0.80, 0.00),
    "Montreal": (0.85, 0.88),
    "Nashville": (0.60, 0.42),
    "New Orleans": (0.55, 0.22),
    "New York": (0.86, 0.75),
    "Oklahoma City": (0.42, 0.40),
    "Omaha": (0.47, 0.58),
    "Phoenix": (0.22, 0.32),
    "Pittsburgh": (0.74, 0.65),
    "Portland": (0.10, 0.85),
    "Raleigh": (0.72, 0.42),
    "Saint Louis": (0.52, 0.50),
    "Salt Lake City": (0.22, 0.55),
    "San Francisco": (0.08, 0.40),
    "Santa Fe": (0.30, 0.38),
    "Sault Ste Marie": (0.62, 0.80),
    "Seattle": (0.07, 0.95),
    "Toronto": (0.77, 0.80),
    "Vancouver": (0.05, 0.97),
    "Washington": (0.78, 0.65),
}

# Définition des routes (Ville1, Ville2, couleur, longueur)
ROUTES_USA = [
    ("Atlanta", "Nashville", "grey", 1),
    ("Atlanta", "Miami", "blue", 5),
    ("Atlanta", "New Orleans", "yellow", 4),
    ("Atlanta", "Charleston", "blue", 2),
    ("Boston", "New York", "yellow", 2),
    ("Boston", "Montreal", "grey", 2),
    ("Calgary", "Helena", "grey", 4),
    ("Calgary", "Seattle", "grey", 4),
    ("Charleston", "Miami", "pink", 4),
    ("Chicago", "Duluth", "red", 3),
    ("Chicago", "Omaha", "blue", 4),
    ("Chicago", "Pittsburgh", "orange", 3),
    ("Chicago", "Saint Louis", "green", 2),
    ("Dallas", "Houston", "grey", 1),
    ("Dallas", "Little Rock", "grey", 2),
    ("Dallas", "Oklahoma City", "grey", 2),
    ("Denver", "Kansas City", "black", 4),
    ("Denver", "Kansas City", "orange", 4),
    ("Denver", "Oklahoma City", "red", 4),
    ("Denver", "Santa Fe", "grey", 2),
    ("Denver", "Salt Lake City", "red", 3),
    ("Duluth", "Omaha", "grey", 2),
    ("Duluth", "Sault Ste Marie", "grey", 3),
    ("Duluth", "Toronto", "pink", 6),
    ("El Paso", "Dallas", "red", 4),
    ("El Paso", "Houston", "green", 6),
    ("El Paso", "Los Angeles", "black", 6),
    ("El Paso", "Oklahoma City", "yellow", 5),
    ("El Paso", "Phoenix", "grey", 3),
    ("Helena", "Denver", "green", 4),
    ("Helena", "Duluth", "orange", 6),
    ("Helena", "Omaha", "red", 5),
    ("Helena", "Salt Lake City", "pink", 3),
    ("Helena", "Seattle", "yellow", 6),
    ("Houston", "New Orleans", "pink", 2),
    ("Kansas City", "Oklahoma City", "grey", 2),
    ("Kansas City", "Saint Louis", "blue", 2),
    ("Las Vegas", "Los Angeles", "grey", 2),
    ("Las Vegas", "Salt Lake City", "orange", 3),
    ("Little Rock", "New Orleans", "green", 3),
    ("Little Rock", "Nashville", "white", 3),
    ("Little Rock", "Oklahoma City", "grey", 2),
    ("Los Angeles", "Phoenix", "grey", 3),
    ("Los Angeles", "San Francisco", "pink", 3),
    ("Los Angeles", "San Francisco", "yellow", 3),
    ("Miami", "New Orleans", "red", 6),
    ("Montreal", "New York", "blue", 3),
    ("Montreal", "Sault Ste Marie", "black", 5),
    ("Nashville", "Pittsburgh", "yellow", 4),
    ("Nashville", "Saint Louis", "grey", 2),
    ("New Orleans", "Houston", "grey", 2),
    ("New Orleans", "Atlanta", "yellow", 4),
    ("New Orleans", "Miami", "red", 6),
    ("New York", "Pittsburgh", "green", 2),
    ("New York", "Washington", "black", 2),
    ("Oklahoma City", "Santa Fe", "blue", 3),
    ("Omaha", "Kansas City", "grey", 1),
    ("Omaha", "Chicago", "blue", 4),
    ("Omaha", "Denver", "pink", 4),
    ("Phoenix", "Santa Fe", "grey", 3),
    ("Pittsburgh", "Saint Louis", "green", 5),
    ("Pittsburgh", "Washington", "grey", 2),
    ("Portland", "Salt Lake City", "blue", 6),
    ("Portland", "San Francisco", "green", 5),
    ("Portland", "Seattle", "grey", 1),
    ("Raleigh", "Charleston", "grey", 2),
    ("Raleigh", "Pittsburgh", "grey", 2),
    ("Raleigh", "Washington", "grey", 2),
    ("Saint Louis", "Kansas City", "blue", 2),
    ("Saint Louis", "Little Rock", "grey", 2),
    ("Saint Louis", "Pittsburgh", "green", 5),
    ("Salt Lake City", "San Francisco", "orange", 5),
    ("Salt Lake City", "Denver", "red", 3),
    ("Salt Lake City", "Helena", "pink", 3),
    ("Salt Lake City", "Las Vegas", "orange", 3),
    ("San Francisco", "Portland", "green", 5),
    ("San Francisco", "Salt Lake City", "orange", 5),
    ("San Francisco", "Los Angeles", "pink", 3),
    ("San Francisco", "Los Angeles", "yellow", 3),
    ("Sault Ste Marie", "Duluth", "grey", 3),
    ("Sault Ste Marie", "Montreal", "black", 5),
    ("Seattle", "Calgary", "grey", 4),
    ("Seattle", "Helena", "yellow", 6),
    ("Seattle", "Portland", "grey", 1),
    ("Toronto", "Duluth", "pink", 6),
    ("Toronto", "Montreal", "grey", 3),
    ("Toronto", "Pittsburgh", "grey", 2),
    ("Vancouver", "Calgary", "grey", 3),
    ("Vancouver", "Seattle", "grey", 1),
    ("Washington", "New York", "black", 2),
    ("Washington", "Pittsburgh", "grey", 2),
]

# Définition des cartes destination (Ville1, Ville2, points)
CARTES_DESTINATION_USA = [
    ("Los Angeles", "New York", 21), ("Duluth", "Houston", 8), ("Chicago", "New Orleans", 7),
    ("New York", "Atlanta", 6), ("Portland", "Nashville", 17), ("Vancouver", "Montreal", 20),
    ("Duluth", "El Paso", 10), ("Winnipeg", "Little Rock", 11), ("San Francisco", "Atlanta", 17),
    ("Kansas City", "Houston", 5), ("Los Angeles", "Miami", 20), ("Denver", "Pittsburgh", 11),
    ("Chicago", "Santa Fe", 9), ("Vancouver", "Santa Fe", 13), ("Calgary", "Phoenix", 13),
    ("Los Angeles", "Chicago", 16), ("Denver", "El Paso", 4), ("New York", "Dallas", 11),
    ("Toronto", "Miami", 10), ("Portland", "Phoenix", 11), ("Dallas", "New York", 11),
    ("Calgary", "Los Angeles", 12), ("Winnipeg", "Houston", 12), ("Montreal", "Atlanta", 9),
    ("Seattle", "New York", 22), ("San Francisco", "New Orleans", 20), ("Kansas City", "Montreal", 13),
    ("Denver", "Chicago", 7), ("Boston", "Miami", 12), ("Chicago", "Los Angeles", 16)
]
#endregion

#region === Classes principales ===

# Classe principale regroupant tout
class Table:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.plateau = Plateau(VILLES_USA, ROUTES_USA)
        self.pioche_wagon = PiocheWagon([CarteWagon(c) for c in ["red", "blue", "green", "yellow", "black", "white", "orange", "pink"] * 12 + ["locomotive"] * 14])
        self.pioche_itineraire = PiocheItineraire([CarteItineraire(v1, v2, p) for v1, v2, p in CARTES_DESTINATION_USA])
        self.score = 0

    def initialiser_partie(self):
        """Distribue les cartes de départ aux joueurs avec restriction de repose à une seule carte maximum."""
        for joueur in self.joueurs:
            joueur.cartes_wagon = [self.pioche_wagon.piocher_cachee() for _ in range(4)]
            cartes_itineraire = self.pioche_itineraire.piocher()

            # Appliquer la restriction de repose d'une seule carte seulement au début
            cartes_gardees, cartes_reposees = joueur.choisir_cartes_itineraire(cartes_itineraire, initialisation=True)

            joueur.cartes_defi.extend(cartes_gardees)  # Ajouter les cartes gardées au joueur

            if cartes_reposees:  # Vérifier si une carte a été reposée
                self.pioche_itineraire.replacer_en_bas(cartes_reposees)  # Replacer en bas de la pioche

    def jouer_tour(self, joueur):
        """Permet à un joueur de jouer son tour avec validation stricte"""
        while True:

            print(f"\n{joueur.nom}, c'est votre tour !")
            # Compter les occurrences des couleurs dans les cartes du joueur
            couleurs_cartes = Counter(c.couleur for c in joueur.cartes_wagon)

            # Afficher les cartes avec leur fréquence
            print("Voici vos cartes wagon :")
            for couleur, count in couleurs_cartes.items():
                print(f"{couleur}: {count}")
            print("Voici vos cartes destination :", [f"{c.ville_depart} → {c.ville_arrivee}" for c in joueur.cartes_defi])
            print(f"Nombre de wagons restants : {joueur.wagons_restants}")

            print("1. Piocher une carte wagon")
            print("2. Capturer une route")
            print("3. Piocher des cartes destination")
            print("4. afficher le plateau")
            print("5. Quitter le jeu")
            choix = input("Choisissez une action (1, 2, 3, 4, 5) : ")

            if choix == "1":
                self.piocher_cartes_wagon(joueur)
                break
            elif choix == "2":
                self.capturer_route(joueur)
                break
            elif choix == "3":
                self.piocher_cartes_itineraire(joueur)
                break
            elif choix == "4":
                self.plateau.afficher_plateau_graphique()
                break
            elif choix == "5":
                print("Fin de la partie. Merci d'avoir joué !")
                exit()
            else:
                print("choix invalide, veuiller reessayer")

    def capturer_route(self, joueur):
        """Permet à un joueur de capturer une route en défaussant les cartes nécessaires"""
        print("\nRoutes disponibles :")
        routes_disponibles = [route for route in self.plateau.routes if route.possesseur is None and joueur.verifier_cartes_wagon(route)]

        if not routes_disponibles:
            print("Aucune route n'est disponible à capturer.")
            return False

        # Afficher les routes disponibles
        for i, route in enumerate(routes_disponibles):
            print(f"{i}: {route.Ville1} → {route.Ville2} ({route.longueur} cases, couleur : {route.couleur})")

        choix = int(input("Choisissez une route à capturer (numéro) : "))

        if choix < 0 or choix >= len(routes_disponibles):
            print("Choix invalide.")
            return False

        route_choisie = routes_disponibles[choix]

        # Défausser les cartes utilisées
        self.defausser_cartes_wagon(joueur, route_choisie)

        # Marquer la route comme occupée
        route_choisie.possesseur = joueur
        joueur.routes_capturees.append(route_choisie)
        joueur.wagons_restants -= route_choisie.longueur
        
        # Actualiser l'affichage du plateau après capture de la route
        self.plateau.afficher_plateau_graphique()  # Mise à jour visuelle du plateau

        print(f"{joueur.nom} a capturé la route {route_choisie.Ville1} → {route_choisie.Ville2}!")
        return True

    def defausser_cartes_wagon(self, joueur, route):
        """Défausse les cartes utilisées pour capturer une route"""
        couleur = route.couleur
        longueur = route.longueur
        cartes_defaussees = []

        # D'abord, utiliser les cartes de la couleur demandée
        for carte in joueur.cartes_wagon[:]:
            if carte.couleur == couleur and longueur > 0:
                cartes_defaussees.append(carte)
                joueur.cartes_wagon.remove(carte)
                longueur -= 1

        # Ensuite, compléter avec des locomotives si nécessaire
        for carte in joueur.cartes_wagon[:]:
            if carte.couleur == "locomotive" and longueur > 0:
                cartes_defaussees.append(carte)
                joueur.cartes_wagon.remove(carte)
                longueur -= 1

        # Ajouter les cartes à la défausse
        for carte in cartes_defaussees:
            self.pioche_wagon.defausser(carte)

    def piocher_cartes_wagon(self, joueur):
        """Gère la pioche de cartes wagon pour un joueur"""
        cartes_piochees, Loco = [], False

        while Loco or len(cartes_piochees) <2 :

            # Affichage des cartes visibles
            print("\nCartes disponibles :")
            for i, carte in enumerate(self.pioche_wagon.visible):
                print(f"{carte.couleur}")
            # Premier tirage
            carte1, pioche = self.choisir_carte_wagon()
            if not carte1:
                print("Aucune carte n'a pu être piochée.")
                return
            cartes_piochees.append(carte1)
            joueur.cartes_wagon.append(carte1)
            print(f"{joueur.nom}, vous avez choisi la carte {carte1.couleur}")

            # Vérifier si c'était une locomotive → Pas de deuxième pioche
            if carte1.is_locomotive and pioche == 1:
                print(f"{joueur.nom} a pioché une locomotive et ne peut pas prendre de deuxième carte. Fin du tour.")
                Loco = True
                return  # ✅ Arrêt immédiat

            # Deuxième tirage
            carte2 = self.choisir_carte_wagon(interdit_locomotive=True) [0]
            cartes_piochees.append(carte2)
            joueur.cartes_wagon.append(carte2)

            print(f"{joueur.nom}, vous avez pioché : {carte1.couleur, carte2.couleur}")

    def choisir_carte_wagon(self, interdit_locomotive=False):
        """Permet au joueur de choisir une carte visible ou cachée avec validation stricte"""

        while True:
            print("\n1. Piocher une carte cachée")
            print("2. Choisir une carte visible")

            choix = input("Choisissez une option (1 ou 2) : ")

            if choix == "1":
                carte = self.pioche_wagon.piocher_cachee()
                print(f"Vous avez pioché une carte {carte.couleur}.")
                return carte, 0

            elif choix == "2":
                self.afficher_cartes_visibles()

                try:
                    index = int(input("Choisissez une carte visible (1-5) : ")) - 1  # ✅ Ajustement pour l’index

                    if index < 0 or index >= len(self.pioche_wagon.visible):
                        print("❌ Choix invalide. Veuillez choisir un numéro entre 1 et 5.")
                        continue  # Redemander

                    carte = self.pioche_wagon.visible.pop(index)

                    if interdit_locomotive and carte.is_locomotive:
                        print("❌ Vous ne pouvez pas prendre une locomotive en deuxième carte !")
                        self.pioche_wagon.visible.insert(index, carte)  # Remettre la carte dans les visibles
                        continue  # Redemander

                    # Remplacement de la carte visible
                    if self.pioche_wagon.pioche:
                        self.pioche_wagon.visible.append(self.pioche_wagon.piocher_cachee())
                        self.pioche_wagon.verifier_visibles_sans_3_locomotives()
                    else:
                        self.pioche_wagon.remelanger_si_vide()
                        self.pioche_wagon.visible.append(self.pioche_wagon.piocher_cachee())
                        self.pioche_wagon.verifier_visibles_sans_3_locomotives()

                    print(f"Vous avez choisi la carte {carte.couleur}.")
                    return carte, 1

                except ValueError:
                    print("❌ Entrée invalide. Veuillez entrer un numéro valide.")

    def piocher_cartes_itineraire(self, joueur):
        """Permet au joueur de piocher 3 cartes destination et d'en garder au moins une."""
        piochees = self.pioche_itineraire.piocher()

        print(f"\n{joueur.nom}, voici vos cartes destination :")
        for i, carte in enumerate(piochees):
            print(f"{i + 1}: {carte.ville_depart} → {carte.ville_arrivee} ({carte.points} points)")

        cartes_a_reposer = []

        # Premier choix : garder toutes les cartes ou en reposer une
        choix = input("Voulez-vous garder les trois cartes (0) ou en reposer une ? (1, 2 ou 3) : ")

        if choix in ["1", "2", "3"]:
            cartes_a_reposer.append(piochees.pop(int(choix) - 1))  # Repose UNE carte

            # Permettre une deuxième repose seulement si au moins 2 cartes restent
            if len(piochees) > 1:
                for i, carte in enumerate(piochees):
                    print("voici les cartes destination qui vous restent :")
                    print(f"{i + 1}: {carte.ville_depart} → {carte.ville_arrivee} ({carte.points} points)")
                choix2 = input("Voulez-vous reposer une autre carte ? (0 = non, sinon 1 ou 2) : ")
                if choix2 in ["1", "2"]:
                    cartes_a_reposer.append(piochees.pop(int(choix2) - 1))  # Repose une deuxième carte

        print(f"{joueur.nom} garde {len(piochees)} carte(s) et repose {len(cartes_a_reposer)} carte(s).")

        # Ajouter les cartes gardées au joueur
        joueur.cartes_defi.extend(piochees)

        # Remettre les cartes rejetées en bas de la pioche
        if cartes_a_reposer:
            self.pioche_itineraire.replacer_en_bas(cartes_a_reposer)

        print(f"{joueur.nom} a maintenant {len(joueur.cartes_defi)} cartes destination.")

    def afficher_cartes_visibles(self):
        """Affiche les cartes visibles avec une numérotation de 1 à 5"""
        print("\nCartes visibles :")
        for i, carte in enumerate(self.pioche_wagon.visible, start=1):  # ✅ Numérotation commence à 1
            print(f"{i}: {carte.couleur}")

    def compte_des_points(self):
        print("\n=== Bilan des scores ===")

        for joueur in self.joueurs:

            points_routes = joueur.calculer_points_routes()
            points_objectifs = joueur.calculer_points_destinations()
            total = points_routes + points_objectifs

            print(f"{joueur.nom} :")
            if joueur == self.joueur_plus_longue_route() :
                print(f"{joueur.nom} remporte le bonus de la route la plus longue.")
                total += 10

            print(f"  Points routes : {points_routes}")
            print(f"  Points objectifs : {points_objectifs}")
            print(f"  Score total : {total}\n")

    def joueur_plus_longue_route(self):
        """Retourne le joueur ayant la plus longue route (sans passer deux fois par la même ville)"""


        def plus_long_chemin(joueur):
            G = self.plateau.sous_graphe_joueur(joueur)
            max_longueur = 0

            # DFS à partir de chaque sommet
            for ville in G.nodes:
                visited = set()
                stack = [(ville, 0, visited)]

                while stack:
                    current, longueur, visited = stack.pop()
                    visited.add(current)
                    max_longueur = max(max_longueur, longueur)

                    for voisin in G.neighbors(current):
                        if voisin not in visited:
                            stack.append((voisin, longueur + 1, visited.copy()))

            return max_longueur

        meilleurs = []
        max_val = -1

        for joueur in self.joueurs:
            longueur = plus_long_chemin(joueur)
            if longueur > max_val:
                meilleurs = [joueur]
                max_val = longueur
            elif longueur == max_val:
                meilleurs.append(joueur)

        if len(meilleurs) == 1:
            return meilleurs[0]
        else:
            return None  # égalité


# Classe représentant un joueur
class Joueur:
    def __init__(self, nom, couleur):
        self.nom = nom
        self.couleur = couleur
        self.routes_capturees = []
        self.cartes_wagon = []  # Cartes wagon en main
        self.cartes_defi = []  # Cartes destination/objectifs
        self.wagons_restants = 45  # Wagons restants au début

    def choisir_cartes_itineraire(self, cartes, initialisation = False):
        """Permet au joueur de garder au moins une carte destination au début du jeu"""
        print(f"\n{self.nom}, voici vos cartes destination initiales :")
        for i, carte in enumerate(cartes):
            print(f"{i + 1}: {carte}")

        cartes_a_reposer = []

        choix = input("Voulez-vous garder les trois cartes (0) ou en reposer une ? (1, 2 ou 3) : ")
        if choix in ["1", "2", "3"]:
            cartes_a_reposer.append(cartes.pop(int(choix) - 1))

        if len(cartes) > 1 and not initialisation:
            choix2 = input("Voulez-vous reposer une autre carte ? (0 = non, sinon 1 ou 2) : ")
            if choix2 in ["1", "2"]:
                cartes_a_reposer.append(cartes.pop(int(choix2) - 1))

        print(f"{self.nom} garde {len(cartes)} carte(s) et repose {len(cartes_a_reposer)} carte(s).")
        return cartes, cartes_a_reposer

    def verifier_cartes_wagon(self, route):
        """Vérifie si le joueur possède les cartes nécessaires pour capturer la route"""
        couleur = route.couleur
        longueur = route.longueur

        # Si la route est grise, autoriser n'importe quelle couleur
        if couleur == "gris":
            cartes_joueur = {c.couleur: self.cartes_wagon.count(c) for c in self.cartes_wagon if
                             c.couleur != "locomotive"}
            meilleure_couleur = max(cartes_joueur, key=cartes_joueur.get, default=None)

            if meilleure_couleur and cartes_joueur[meilleure_couleur] + self.cartes_wagon.count(
                    "locomotive") >= longueur:
                return True
        else:
            cartes_joueur = {c.couleur: self.cartes_wagon.count(c) for c in self.cartes_wagon}
            locomotives = cartes_joueur.get("locomotive", 0)
            cartes_route = cartes_joueur.get(couleur, 0)

            if cartes_route + locomotives >= longueur:
                return True

        return False

    def calculer_points_routes(self):
        points = 0
        for route in self.routes_capturees:
            if route.longueur == 1:
                points += 1
            elif route.longueur == 2:
                points += 2
            elif route.longueur == 3:
                points += 4
            elif route.longueur == 4:
                points += 7
            elif route.longueur == 5:
                points += 10
            elif route.longueur == 6:
                points += 15
        return points

    def villes_reliees(self, ville_depart, ville_arrivee):
        """Vérifie si deux villes sont reliées par les routes capturées par ce joueur."""
        G = nx.Graph()

        for route in self.routes_capturees:
            G.add_edge(route.Ville1, route.Ville2)

        try:
            return nx.has_path(G, ville_depart, ville_arrivee)
        except nx.NetworkXError:
            return False

    def calculer_points_destinations(self):
            points = 0
            for destination in self.cartes_defi:
                if self.villes_reliees(destination.ville_depart, destination.ville_arrivee):
                    print(f"Objectif réussi : {destination.ville_depart} → {destination.ville_arrivee} (+{destination.points} points)")
                    points += destination.points
                else:
                    print(f"Objectif échoué : {destination.ville_depart} → {destination.ville_arrivee} (+{destination.points} points)")
                    points -= destination.points
            return points

#endregion

#region === Classes Cartes ===

# Classe regroupant les différentes cartes
class Carte:
    def __str__(self):
        return "Carte"

# Classe représentant les cartes wagon
class CarteWagon(Carte):
    def __init__(self, couleur):
        self.couleur = couleur
        self.is_locomotive = (couleur == "locomotive")  # Ajout d’un flag pour éviter des vérifications de texte

    def __str__(self):
        return f"Carte Wagon ({self.couleur})"

# Classe représentant les cartes itinéraire
class CarteItineraire(Carte):
    def __init__(self, ville_depart, ville_arrivee, points):
        self.ville_depart = ville_depart
        self.ville_arrivee = ville_arrivee
        self.points = points
        self.possesseur = None  # Joueur possédant cette carte

    def __str__(self):
        return f"{self.ville_depart} → {self.ville_arrivee} ({self.points} points)"

#endregion

#region === Classes Pioches ===

# Classe regroupant les différentes pioches
class Pioche:
    def __init__(self, cartes):
        self.pioche = cartes  # Liste des cartes wagon
        random.shuffle(self.pioche)

# Classe représentant la pioche des cartes Wagon
class PiocheWagon(Pioche):
    def __init__(self, cartes):
        super().__init__(cartes)
        self.visible = [self.pioche.pop() for _ in range(5)]  # 5 cartes visibles
        self.defausse = []

    def piocher_visible(self, index):
        """Pioche une carte visible et la remplace par une carte de la pioche cachée."""
        if 0 <= index < len(self.visible):
            carte = self.visible.pop(index)
            self.remelanger_si_vide()  # Vérifier et mélanger si nécessaire
            if self.pioche:
                self.visible.append(self.pioche.pop())
                self.verifier_visibles_sans_3_locomotives()
            return carte
        return None

    def piocher_cachee(self):
        """Pioche une carte face cachée en vérifiant si un mélange est nécessaire."""
        self.remelanger_si_vide()  # Vérifier et mélanger si la pioche est vide
        return self.pioche.pop() if self.pioche else None

    def defausser(self, carte):
        """Ajoute une carte à la défausse."""
        self.defausse.append(carte)

    def remelanger_si_vide(self):
        """Mélange la défausse et les cartes visibles si la pioche cachée est vide."""
        if not self.pioche:  # Si la pioche cachée est vide
            print("🔄 Mélange de toutes les cartes (y compris visibles)...")
            self.pioche = self.visible + self.defausse
            self.visible = []
            self.defausse = []
            random.shuffle(self.pioche)

    def verifier_visibles_sans_3_locomotives(self):
        """Vérifie que la pioche visible ne contient pas 3 locomotives.
        Si c'est le cas, mélange les cartes visibles et cachées (sans toucher à la défausse)."""
        nb_locomotives = sum(1 for carte in self.visible if carte.is_locomotive)
        if nb_locomotives >= 3:  # 3 locomotives ou plus, on remélange
            print("DEBUG: Trop de locomotives visibles ! Mélange en cours...")
            self.pioche.extend(self.visible)  # Remet les visibles dans la pioche cachée
            self.visible.clear()
            random.shuffle(self.pioche)

            # Reprendre 5 nouvelles cartes visibles
            for _ in range(5):
                if self.pioche:
                    self.visible.append(self.pioche.pop())

            print(f"DEBUG: Nouvelle pioche visible après correction: {[c.couleur for c in self.visible]}")

# Classe représentant la pioche de cartes itinéraires
class PiocheItineraire(Pioche):
    def __init__(self, cartes):
        super().__init__(cartes)

    def piocher(self):
        """Pioche trois cartes destination."""
        return [self.pioche.pop() for _ in range(min(3, len(self.pioche)))]

    def replacer_en_bas(self, cartes):
        """Replace les cartes non gardées en bas de la pioche."""
        self.pioche = cartes + self.pioche

#endregion

#region === Classes Plateau ===

# Classe représentant le plateau de jeu (toutes les villes et les routes)
class Plateau:
    def __init__(self, dico_ville, dico_route):
        self.villes = [Ville(nom, coordonnees=dico_ville[nom]) for nom in dico_ville]
        self.dico_villes = {ville.nom: ville for ville in self.villes}
        self.routes = [Route(self.dico_villes[V1], self.dico_villes[V2], couleur, longueur) for V1, V2, couleur, longueur in dico_route]
        self.afficher_plateau_graphique()

    def double(self, route):
        """Renvoie True si une autre route relie les mêmes villes (dans un sens ou dans l’autre)"""
        v1, v2 = route.Ville1.nom, route.Ville2.nom

        for autre in self.routes:
            if autre is route:
                continue
            # comparer sans tenir compte de l'ordre
            villes = {autre.Ville1.nom, autre.Ville2.nom}
            if {v1, v2} == villes:
                return True

        return False

    def sous_graphe_joueur(self, joueur):
        G = nx.Graph()
        for route in self.routes:  # toutes les routes du plateau
            if route.possesseur == joueur:
                G.add_edge(route.Ville1.nom, route.Ville2.nom)
        return G

    def afficher_plateau_graphique_rect(self): #ebauche de visualisation des routes avec des rectangles
        plt.figure(figsize=(12, 8))

        for ville in self.villes:
            x, y = ville.coordonnees
            plt.plot(x, y, 'o', color='black')
            plt.text(x, y + 0.3, ville.nom, ha='center', fontsize=8)

        for route in self.routes:
            x1, y1 = route.Ville1.coordonnees
            x2, y2 = route.Ville2.coordonnees

            dx, dy = x2 - x1, y2 - y1
            L = np.sqrt(dx ** 2 + dy ** 2)
            ux, uy = dx / L, dy / L  # vecteur direction unitaire
            px, py = -uy * 0.2, ux * 0.2  # vecteur perpendiculaire pour double route

            # Couleur de la bordure (route) et remplissage
            border_color = route.couleur
            fill_color = "white" if route.possesseur is None else route.possesseur.couleur

            # Décalage si route double
            offset = (px, py) if getattr(route, "double", False) else (0, 0)

            # Tracer les wagons
            wagon_length = 0.025  # en unité normalisée, pour un plateau [0, 1]
            wagon_height = 0.012

            total_wagon_length = wagon_length * route.longueur
            gap = (L - total_wagon_length) / (route.longueur + 1)

            for i in range(route.longueur):
                d = gap * (i + 1) + wagon_length * i + wagon_length / 2
                cx = x1 + d * ux + offset[0]
                cy = y1 + d * uy + offset[1]

                angle = np.degrees(np.arctan2(dy, dx))
                rect = patches.Rectangle(
                    (cx - wagon_length / 2, cy - wagon_height / 2),
                    wagon_length,
                    wagon_height,
                    angle=angle,
                    linewidth=2.5,
                    edgecolor=border_color,
                    facecolor=fill_color
                )
                plt.gca().add_patch(rect)

        plt.axis('equal')
        plt.axis('off')
        plt.title("Plateau des Aventuriers du Rail — affichage par wagons")
        plt.show()

    def afficher_plateau_graphique(self):
        G = nx.Graph()

        # Ajouter les villes comme nœuds
        for ville in self.villes:
            G.add_node(ville.nom, pos=(ville.coordonnees[0], ville.coordonnees[1]))  # (abcisse, ordonnée)

        # Ajouter les routes comme arêtes
        for route in self.routes:
            color = route.couleur if route.etat == "disponible" else "purple"  # Couleur normale ou gris pour les capturées
            style = "solid" if route.etat == "disponible" else "dotted"  # Style de ligne
            G.add_edge(route.Ville1, route.Ville2, color=color, style=style, weight=route.longueur)

        # Préparer l'affichage
        pos = nx.get_node_attributes(G, 'pos')
        couleurs = [G[u][v]['color'] for u, v in G.edges()]
        styles = [G[u][v].get('style', 'solid') for u, v in G.edges()]  # Récupère le style de chaque arête
        poids = [G[u][v]['weight'] for u, v in G.edges()]
        
        # Ajouter des annotations si une route est capturée
        for route in self.routes:
            if route.etat == "capturée":
                x_pos = (pos[route.Ville1][0] + pos[route.Ville2][0]) / 2
                y_pos = (pos[route.Ville1][1] + pos[route.Ville2][1]) / 2
                plt.text(x_pos, y_pos, "capturée", fontsize=10, ha='center', color="black")


        # Afficher
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, edge_color=couleurs, width=poids, node_size=500, font_size=8, style = styles)
        plt.title("Plateau des Aventuriers du Rail (Version USA)")
        plt.show()

# Classe représentant une ville
class Ville:
    def __init__(self, nom, coordonnees=None):
        self.nom = nom
        self.coordonnees = coordonnees  # Coordonnées optionnelles (x, y) pour affichage graphique

# Classe représentant une route entre deux villes
class Route:

    def __init__(self, Ville1, Ville2, couleur, longueur):
        self.Ville1 = Ville1
        self.Ville2 = Ville2
        self.longueur = longueur
        self.couleur = couleur
        self.possesseur = None
        self.etat = "disponible"  # Par défaut, la route est disponible

    def capturer(self, joueur):
        """Marque la route comme capturée par un joueur."""
        self.possesseur = joueur
        self.etat = "capturée"  # Change l'état de la route à "capturée"

#endregion
