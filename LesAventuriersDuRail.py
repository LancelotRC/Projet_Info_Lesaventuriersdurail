#region === Imports ===

import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from collections import Counter
import builtins
import json
import sys
from PIL import Image
from matplotlib import image as mpimg

#endregion
COULEURS_MATPLOTLIB = {
    "rouge": "red",
    "bleu": "blue",
    "vert": "green",
    "jaune": "yellow",
    "noir": "black",
    "blanc": "white",
    "rose": "pink",
    "orange": "orange",
    "locomotive": "gray",  # facultatif, visuel pour les locomotives
}

#region === definition des données pour le jeu version USA ===
VILLES_USA_normalised = {
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
    "Winnipeg": (0.38, 0.94),
    "Washington": (0.78, 0.65),
}

# Définition des villes du plateau USA
VILLES_USA = {
    "Atlanta": (594, 327),
    "Boston": (725,107),
    "Calgary": (177,70),
    "Charleston": (667,332),
    "Chicago": (519, 211),
    "Dallas": (420, 401),
    "Denver": (296, 284),
    "Duluth": (428, 164),
    "El Paso": (286, 419),
    "Helena": (252, 169),
    "Houston": (451, 431),
    "Kansas City": (420, 271),
    "Las Vegas": (158, 342),
    "Little Rock": (473, 338),
    "Los Angeles": (108, 387),
    "Miami": (692,453),
    "Montreal": (670,63),
    "Nashville": (556, 301),
    "New Orleans": (523, 425),
    "New York": (684,164),
    "Oklahoma City": (406, 336),
    "Omaha": (405, 233),
    "Phoenix": (199,390),
    "Pittsburgh": (619, 199),
    "Portland": (62, 162),
    "Raleigh": (645,284),
    "Saint Louis": (486, 272),
    "Salt Lake City": (198,261),
    "San Francisco": (54,307),
    "Santa Fe": (290,351),
    "Sault Ste Marie": (523, 114),
    "Seattle": (78,124),
    "Toronto": (606, 129),
    "Vancouver": (80,80),
    "Winnipeg": (347, 76),
    "Washington": (690, 233),
}


# Définition des routes (Ville1, Ville2, couleur, longueur)
ROUTES_USA = [
    ("Vancouver", "Calgary", "grey", 3, False),
    ("Vancouver", "Seattle", "grey", 1, True),
    ("Vancouver", "Seattle", "grey", 1, True),
    ("Seattle", "Calgary", "grey", 4, False),
    ("Seattle", "Portland", "grey", 1, True),
    ("Seattle", "Portland", "grey", 1, True),
    ("Portland", "Salt Lake City", "blue", 6, False),
    ("Portland", "San Francisco", "green", 5, True),
    ("Portland", "San Francisco", "green", 5, True),
    ("San Francisco", "Salt Lake City", "orange", 5, True),
    ("San Francisco", "Salt Lake City", "white", 5, True),
    ("San Francisco", "Los Angeles", "pink", 3, True),
    ("San Francisco", "Los Angeles", "yellow", 3, True),
    ("Los Angeles", "Las Vegas", "grey", 2, False),
    ("Los Angeles", "Phoenix", "grey", 3, False),
    ("Los Angeles", "El Paso", "black", 6, False),
    ("Calgary", "Winnipeg", "white", 5, False),
    ("Helena", "Winnipeg", "blue", 4, False),
    ("Helena", "Seattle", "yellow", 6, False),
    ("Helena", "Calgary", "grey", 4, False),
    ("Helena", "Denver", "green", 4, False),
    ("Helena", "Duluth", "orange", 6, False),
    ("Helena", "Omaha", "red", 5, False),
    ("Helena", "Salt Lake City", "pink", 3, False),
    ("Salt Lake City", "Denver", "red", 3, True),
    ("Salt Lake City", "Denver", "yellow", 3, True),
    ("Salt Lake City", "Las Vegas", "orange", 3, False),
    ("Phoenix", "El Paso", "grey", 3, False),
    ("Phoenix", "Santa Fe", "grey", 3, False),
    ("Phoenix", "Denver", "white", 3, False),
    ("Denver", "Kansas City", "black", 4, True),
    ("Denver", "Kansas City", "orange", 4, True),
    ("Denver", "Oklahoma City", "red", 4, False),
    ("Denver", "Santa Fe", "grey", 2, False),
    ("Denver", "Omaha", "pink", 4, False),
    ("Santa Fe", "Oklahoma City", "blue", 3, False),
    ("Santa Fe", "El Paso", "grey", 3, False),
    ("El Paso", "Dallas", "red", 4, False),
    ("El Paso", "Houston", "green", 6, False),
    ("El Paso", "Oklahoma City", "yellow", 5, False),
    ("Winnipeg", "Sault Ste Marie", "grey", 6, False),
    ("Winnipeg", "Duluth", "black", 6, False),
    ("Duluth", "Omaha", "grey", 2, True),
    ("Duluth", "Omaha", "grey", 2, True),
    ("Duluth", "Sault Ste Marie", "grey", 3, False),
    ("Duluth", "Toronto", "pink", 6, False),
    ("Duluth", "Chicago", "red", 3, False),
    ("Omaha", "Kansas City", "grey", 1, True),
    ("Omaha", "Kansas City", "grey", 1, True),
    ("Omaha", "Chicago", "blue", 4, False),
    ("Kansas City", "Saint Louis", "blue", 2, True),
    ("Kansas City", "Saint Louis", "pink", 2, True),
    ("Kansas City", "Oklahoma City", "grey", 2, True),
    ("Kansas City", "Oklahoma City", "grey", 2, True),
    ("Oklahoma City", "Dallas", "grey", 2, True),
    ("Oklahoma City", "Dallas", "grey", 2, True),
    ("Oklahoma City", "Little Rock", "grey", 2, False),
    ("Dallas", "Houston", "grey", 1, True),
    ("Dallas", "Houston", "grey", 1, True),
    ("Dallas", "Little Rock", "grey", 2, False),
    ("Houston", "New Orleans", "grey", 2, False),
    ("Little Rock", "New Orleans", "green", 3, False),
    ("Little Rock", "Saint Louis", "grey", 2, False),
    ("Little Rock", "Nashville", "white", 3, False),
    ("Saint Louis", "Nashville", "grey", 2, False),
    ("Saint Louis", "Pittsburgh", "green", 5, False),
    ("Saint Louis", "Chicago", "green", 2, False),
    ("Chicago", "Pittsburgh", "orange", 3, True),
    ("Chicago", "Pittsburgh", "black", 3, True),
    ("Chicago", "Toronto", "white", 4, False),
    ("Sault Ste Marie", "Montreal", "black", 5, False),
    ("Sault Ste Marie", "Toronto", "grey", 2, False),
    ("Toronto", "Pittsburgh", "grey", 2, False),
    ("Toronto", "Montreal", "grey", 3, False),
    ("Montreal", "New York", "blue", 3, False),
    ("Montreal", "Boston", "grey", 2, True),
    ("Montreal", "Boston", "grey", 2, True),
    ("Boston", "New York", "yellow", 2, True),
    ("Boston", "New York", "red", 2, True),
    ("New York", "Pittsburgh", "green", 2, True),
    ("New York", "Pittsburgh", "white", 2, True),
    ("New York", "Washington", "black", 2, True),
    ("New York", "Washington", "orange", 2, True),
    ("Pittsburgh", "Washington", "grey", 2, False),
    ("Pittsburgh", "Raleigh", "grey", 2, False),
    ("Pittsburgh", "Nashville", "yellow", 4, False),
    ("Raleigh", "Charleston", "grey", 2, False),
    ("Raleigh", "Washington", "grey", 2, True),
    ("Raleigh", "Washington", "grey", 2, True),
    ("Raleigh", "Nashville", "black", 3, False),
    ("Raleigh", "Atlanta", "grey", 3, True),
    ("Raleigh", "Atlanta", "grey", 3, True),
    ("Atlanta", "Nashville", "grey", 1, False),
    ("Atlanta", "Miami", "blue", 5, False),
    ("Atlanta", "New Orleans", "yellow", 4, True),
    ("Atlanta", "New Orleans", "orange", 4, True),
    ("Atlanta", "Charleston", "grey", 2, False),
    ("Miami", "Charleston", "pink", 4, False),
    ("Miami", "New Orleans", "red", 6, False),
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
        self.pioche_itineraire = PiocheItineraire([CarteItineraire(self.plateau.dico_villes[v1], self.plateau.dico_villes[v2], p) for v1, v2, p in CARTES_DESTINATION_USA])
        self.score = 0

    def initialiser_partie(self):
        """Distribue les cartes de départ aux joueurs avec restriction de repose à une seule carte maximum."""
        for joueur in self.joueurs:
            joueur.cartes_wagon = [self.pioche_wagon.piocher_cachee() for _ in range(4)]
            cartes_itineraire = self.pioche_itineraire.piocher()

            # Appliquer la restriction de repose d'une seule carte seulement au début
            if isinstance(joueur, JoueurAuto):
                cartes_gardees, cartes_reposees = cartes_itineraire, [] # on ne laisse pas le choix au joueur auto
            else:
                cartes_gardees, cartes_reposees = joueur.choisir_cartes_itineraire(cartes_itineraire, initialisation=True)

            joueur.cartes_defi.extend(cartes_gardees)  # Ajouter les cartes gardées au joueur

            if cartes_reposees:  # Vérifier si une carte a été reposée
                self.pioche_itineraire.replacer_en_bas(cartes_reposees)  # Replacer en bas de la pioche

    def jouer_tour(self, joueur):
        """Permet à un joueur de jouer son tour avec validation stricte"""
        while True:
            print("\n")

            self.afficher_cartes_visibles()

            print(f"\n{joueur.nom}, c'est votre tour !")
            # Compter les occurrences des couleurs dans les cartes du joueur
            couleurs_cartes = Counter(c.couleur for c in joueur.cartes_wagon)

            # Afficher les cartes avec leur fréquence
            print("Voici vos cartes wagon :")
            for couleur, count in couleurs_cartes.items():
                print(f"{couleur}: {count}")
            print("Voici vos cartes destination :", [f"{c.ville_depart.nom} → {c.ville_arrivee.nom}" for c in joueur.cartes_defi])
            print(f"Nombre de wagons restants : {joueur.wagons_restants}")
            print("1. Piocher une carte wagon")
            print("2. Capturer une route")
            print("3. Piocher des cartes destination")
            print("4. afficher le plateau")
            print("5. Quitter le jeu")
            choix = input("Choisissez une action (1, 2, 3, 4, 5) : ")

            if choix == "1":
                out = self.piocher_cartes_wagon(joueur)
                if out == None:
                    self.capturer_route(joueur)
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
                self.choisir_si_enregistrer(joueur)
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
            print(f"{i}: {route.Ville1.nom} → {route.Ville2.nom} ({route.longueur} cases, couleur : {route.couleur})")

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

        print(f"{joueur.nom} a capturé la route {route_choisie.Ville1.nom} → {route_choisie.Ville2.nom}!")
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

        if self.pioche_wagon.pioche == []:
            print("plus de cartes wagon disponibles")
            return None

        while Loco or len(cartes_piochees) <2 :

            # Affichage des cartes visibles
            print("\nCartes disponibles :")
            for i, carte in enumerate(self.pioche_wagon.visible):
                print(f"{carte.couleur}")
            # Premier tirage
            carte1, pioche = self.choisir_carte_wagon()
            if not carte1:
                print("Aucune carte n'a pu être piochée.")
                return None
            cartes_piochees.append(carte1)
            joueur.cartes_wagon.append(carte1)
            print(f"{joueur.nom}, vous avez choisi la carte {carte1.couleur}")

            # Vérifier si c'était une locomotive → Pas de deuxième pioche
            if carte1.is_locomotive and pioche == 1:
                print(f"{joueur.nom} a pioché une locomotive et ne peut pas prendre de deuxième carte. Fin du tour.")
                Loco = True
                return  Loco# ✅ Arrêt immédiat

            # Deuxième tirage
            carte2 = self.choisir_carte_wagon(interdit_locomotive=True) [0]
            cartes_piochees.append(carte2)
            joueur.cartes_wagon.append(carte2)

            print(f"{joueur.nom}, vous avez pioché : {carte1.couleur, carte2.couleur}")
            return True

    def choisir_carte_wagon(self, interdit_locomotive=False):
        """Permet au joueur de choisir une carte visible ou cachée avec validation stricte"""

        while True:
            self.afficher_cartes_visibles()
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
                        print("Choix invalide. Veuillez choisir un numéro entre 1 et 5.")
                        continue  # Redemander

                    carte = self.pioche_wagon.visible.pop(index)

                    if interdit_locomotive and carte.is_locomotive:
                        print("Vous ne pouvez pas prendre une locomotive en deuxième carte !")
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
                    print("Entrée invalide. Veuillez entrer un numéro valide.")


            
            
    def sauvegarder(self):
        """Sauvegarde l'état de la partie dans un fichier JSON"""
        donnees = {
            "joueurs": [
                {
                    "nom": j.nom,
                    "couleur": j.couleur,
                    "wagons_restants": j.wagons_restants,
                    "cartes_wagon": j.cartes_wagon if isinstance(j.cartes_wagon[0], str) else [c.couleur for c in j.cartes_wagon],
                    "cartes_defi": [
                        {
                            "ville_depart": c.ville_depart.nom,
                            "ville_arrivee": c.ville_arrivee.nom,
                            "points": c.points
                            }
                        for c in j.cartes_defi
                    ],
                    "routes_capturees": [
                        {
                            "ville1": r.Ville1.nom,
                            "ville2": r.Ville2.nom,
                            "couleur": r.couleur,
                            "longueur": r.longueur
                            }
                        for r in j.routes_capturees
                        ]
                    }
                    for j in self.joueurs
                ],
                "joueur_actuel": self.joueurs.index(self.joueur_actuel) if hasattr(self, "joueur_actuel") else 0
            }
        
        with open("sauvegarde.json", "w") as f:
            json.dump(donnees, f, indent=4)
            print("Partie enregistrée dans 'sauvegarde.json'.")

            
    @classmethod
    def charger_partie(cls, fichier="sauvegarde.json"):
        """Charge une partie à partir d'un fichier JSON"""
        with open(fichier, "r") as f:
            data = json.load(f)

        # Création des joueurs
        joueurs = []
        for j_data in data["joueurs"]:
            j = Joueur(j_data["nom"], j_data["couleur"])
            j.wagons_restants = j_data["wagons_restants"]
            j.cartes_wagon = [CarteWagon(couleur) for couleur in j_data.get("cartes_wagon", [])]
            joueurs.append(j)
            
            # Création de la table et du plateau
        table = cls(joueurs)
        table.plateau = Plateau(VILLES_USA, ROUTES_USA)
        
        # Restaurer les cartes visibles
        table.cartes_visibles = [CarteWagon(couleur) for couleur in data.get("cartes_visibles", [])]

        # Restaurer le joueur actuel (si présent)
        index = data.get("joueur_actuel", 0)
        table.joueur_actuel = table.joueurs[index]
        
        # Reconstruction des cartes itinéraire (objectifs)
        for j, j_data in zip(joueurs, data["joueurs"]):
            j.cartes_defi = [
                CarteItineraire(
                    table.plateau.dico_villes[d["ville_depart"]],
                    table.plateau.dico_villes[d["ville_arrivee"]],
                    d["points"]
                )
                for d in j_data["cartes_defi"]
            ]

            # Stocke temporairement les routes capturées pour chaque joueur
            j.routes_a_restaurer = j_data["routes_capturees"]

        # Restaurer les routes capturées sur le plateau
        for joueur in joueurs:
            for r_data in joueur.routes_a_restaurer:
                for route in table.plateau.routes:
                    if (
                        {route.Ville1.nom, route.Ville2.nom} ==
                        {r_data["ville1"], r_data["ville2"]} and
                        route.longueur == r_data["longueur"]
                    ):
                        route.possesseur = joueur
                        route.etat = "capturée"
                        joueur.routes_capturees.append(route)
                        break

        print("✅ Partie chargée depuis 'sauvegarde.json'")
        return table

                       
                    
    def choisir_si_enregistrer(self, joueur):
        """Permet au joueur de choisir s'il veut enregistrer ou quitter"""
        while True:
            print(f"\n{joueur.nom}, vous avez choisi de quitter le jeu.")
            print("Souhaitez-vous enregistrer la partie ?")
            print("1. Oui")
            print("0. Non")
            choix = input("Votre choix : ")

            if choix == "0":
                print("Partie non enregistrée. Merci d'avoir joué !")
                sys.exit()
            elif choix == "1":
                self.sauvegarder()
                print("Partie enregistrée avec succès. À bientôt !")
                sys.exit()
            else:
                print("Saisie invalide. Veuillez entrer 0 ou 1.")

            


    def piocher_cartes_itineraire(self, joueur):
        """Permet au joueur de piocher 3 cartes destination et d'en garder au moins une."""
        piochees = self.pioche_itineraire.piocher()

        print(f"\n{joueur.nom}, voici vos cartes destination :")
        for i, carte in enumerate(piochees):
            print(f"{i + 1}: {carte.ville_depart.nom} → {carte.ville_arrivee.nom} ({carte.points} points)")

        cartes_a_reposer = []

        # Premier choix : garder toutes les cartes ou en reposer une
        choix = input("Voulez-vous garder les trois cartes (0) ou en reposer une ? (1, 2 ou 3) : ")

        if choix in ["1", "2", "3"]:
            cartes_a_reposer.append(piochees.pop(int(choix) - 1))  # Repose UNE carte

            # Permettre une deuxième repose seulement si au moins 2 cartes restent
            if len(piochees) > 1:
                for i, carte in enumerate(piochees):
                    print("voici les cartes destination qui vous restent :")
                    print(f"{i + 1}: {carte.ville_depart.nom} → {carte.ville_arrivee.nom} ({carte.points} points)")
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

    def afficher_routes_disponibles(self) -> None:
        print("\nRoutes restantes à capturer :")
        for route in self.plateau.routes:
            if route.possesseur is None:
                print(f"- {route.Ville1.nom} → {route.Ville2.nom} ({route.longueur} cases, {route.couleur})")

    def compte_des_points(self,plateau):
        print("\n=== Bilan des scores ===")

        for joueur in self.joueurs:

            points_routes = joueur.calculer_points_routes()
            points_objectifs = joueur.calculer_points_destinations(plateau)
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
        cartes_joueur = Counter(c.couleur for c in self.cartes_wagon)

        locomotives = cartes_joueur.get("locomotive", 0)

        if couleur == "gris":
            # On cherche la meilleure couleur disponible
            non_loco = {c: n for c, n in cartes_joueur.items() if c != "locomotive"}
            if not non_loco:
                return False

            meilleure_couleur = max(non_loco, key=non_loco.get)
            total = non_loco[meilleure_couleur] + locomotives

            if total >= longueur:
                print(f"assez de cartes : {meilleure_couleur} + {locomotives}")
                return True
        else:
            total = cartes_joueur.get(couleur, 0) + locomotives
            if total >= longueur:
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

    def villes_reliees(self, ville_depart, ville_arrivee,plateau):
        """Vérifie si deux villes sont reliées par les routes capturées par ce joueur."""
        G = nx.Graph()
        
        for ville in plateau.villes :
            G.add_node(ville.nom)
        
        for route in self.routes_capturees:
            G.add_edge(route.Ville1.nom, route.Ville2.nom)

        try:
            return nx.has_path(G, ville_depart.nom, ville_arrivee.nom)
        except nx.NetworkXError:
            return False

    def calculer_points_destinations(self,plateau):
            points = 0
            for destination in self.cartes_defi:
                if self.villes_reliees(destination.ville_depart, destination.ville_arrivee, plateau):
                    print(f"Objectif réussi : {destination.ville_depart.nom} → {destination.ville_arrivee.nom} (+{destination.points} points)")
                    points += destination.points
                else:
                    print(f"Objectif échoué : {destination.ville_depart.nom} → {destination.ville_arrivee.nom} (+{destination.points} points)")
                    points -= destination.points
            return points

    def afficher_son_graphe(self):
        G = nx.Graph()
        for route in self.routes_capturees:
            G.add_edge(route.Ville1, route.Ville2, weight=route.longueur, color=route.couleur)

        pos = {ville: VILLES_USA[ville] for ville in G.nodes}
        couleurs = [G[u][v]['color'] for u, v in G.edges()]
        poids = [G[u][v]['weight'] for u, v in G.edges()]

        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, with_labels=True, edge_color=couleurs, width=poids, node_size=300, font_size=8)
        plt.title(f"Routes capturées par {self.nom}")
        plt.show()

class JoueurAuto(Joueur):
    def __init__(self, nom, couleur):
        super().__init__(nom, couleur)

    def jouer_automatiquement(self, table):
        """Remplace temporairement input par une version automatique pour ce tour"""
        original_input = builtins.input
        builtins.input = self.repond_automatiquement
        try:
            table.jouer_tour(self)
        finally:
            builtins.input = original_input

    def repond_automatiquement(self, prompt):
        prompt = prompt.lower()

        if "action" in prompt:
            return self.choisir_action()
        elif "carte visible" in prompt:
            return str(random.randint(1, 5))  # 1 à 5
        elif "option" in prompt:
            return random.choice(["1", "2"])  # cachee ou visible
        elif "voulez-vous garder les trois" in prompt:
            return random.choice(["0", "1", "2", "3"])
        elif "reposer une autre carte" in prompt:
            return random.choice(["0", "1", "2"])
        elif "route à capturer" in prompt:
            # Cherche tous les entiers affichés au début des lignes pour estimer combien de routes sont listées
            lignes = prompt.split("\n")
            indices_valides = [
                int(ligne.split(":")[0]) for ligne in lignes
                if ligne.strip() and ligne[0].isdigit() and ":" in ligne
            ]
            if indices_valides:
                return str(random.choice(indices_valides))
            else:
                return "0"
        else:
            return "0"  # valeur par défaut

    def choisir_action(self):
        nb_cartes = len(self.cartes_wagon)
        total_cartes_possibles = 110  # 8*12 + 14 locomotives

        # proportion de la main
        ratio_main = nb_cartes / total_cartes_possibles

        # pondération de la probabilité de capturer une route
        if nb_cartes < 3:
            proba_capturer = 0.1
        elif nb_cartes <= 6:
            proba_capturer = 0.1 + 0.1 * (nb_cartes - 2)  # de 10% à 50%
        else:
            # entre 7 et total possible, monte de 50% jusqu'à 75%-95%
            if ratio_main < 0.25:
                proba_capturer = 0.75
            elif ratio_main < 0.5:
                proba_capturer = 0.9
            else:
                proba_capturer = 0.95

        # tirage au sort pondéré
        if random.random() < proba_capturer:
            return "2"  # capturer une route
        else:
            return "1" #piocher


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

    # def __str__(self):
    #     return f"{self.ville_depart.nom} → {self.ville_arrivee.nom} ({self.points} points)"
    def __str__(self):
        dep = self.ville_depart.nom if hasattr(self.ville_depart, "nom") else self.ville_depart
        arr = self.ville_arrivee.nom if hasattr(self.ville_arrivee, "nom") else self.ville_arrivee
        return f"{dep} → {arr} ({self.points} points)"


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
        self.routes = [Route(self.dico_villes[V1], self.dico_villes[V2], couleur, longueur, double) for V1, V2, couleur, longueur, double in dico_route]
        self.afficher_plateau_graphique()


    def sous_graphe_joueur(self, joueur):
        G = nx.Graph()
        for route in self.routes:  # toutes les routes du plateau
            if route.possesseur == joueur:
                G.add_edge(route.Ville1.nom, route.Ville2.nom)
        return G

    def afficher_plateau_graphique(self):
        #visualisation des routes avec des rectangles
        fig, ax = plt.subplots(figsize=(11.74, 7.42))

        #fig.patch.set_facecolor("#faf0e6")
        #ax.set_facecolor("#faf0e6")
        #ax.patch.set_facecolor("#faf0e6")
        img = mpimg.imread("plateau.png")
        img_flipped = np.flipud(img)
        ax.imshow(img_flipped, extent=[0, 768, 0, 517], zorder=0)
        ax.invert_yaxis()

        for ville in self.villes:
            x, y = ville.coordonnees
            ax.plot(x, y, 'o', color='black')
            ax.text(x, y, ville.nom, ha='center', fontsize=8)

        i = 1

        for route in self.routes:

            x1, y1 = route.Ville1.coordonnees
            x2, y2 = route.Ville2.coordonnees

            dx, dy = x2 - x1, y2 - y1
            L = np.sqrt(dx ** 2 + dy ** 2)
            ux, uy = dx / L, dy / L  # vecteur direction unitaire
            norme = np.sqrt(ux ** 2 + uy ** 2)
            px, py = (-uy / norme) * 5, (ux / norme) * 5

            # Couleur de la bordure (route) et remplissage
            border_color = COULEURS_MATPLOTLIB.get(route.couleur, "gray")

            if route.possesseur is None:
                fill_color = "white"
            else:
                fill_color = COULEURS_MATPLOTLIB.get(route.possesseur.couleur, "gray")


            # Tracer les wagons
            wagon_length = 23
            wagon_height = 7

            total_wagon_length = wagon_length * route.longueur
            gap = (L - total_wagon_length) / (route.longueur + 1)

            if route.double :
                i = -i

            for j in range(route.longueur):
                d = gap * (j + 1) + wagon_length * j + wagon_length / 2

                fraction = (j + 1) / (route.longueur + 1)
                cx = x1 + fraction * dx
                cy = y1 + fraction * dy
                if route.double:
                    cx += px*i
                    cy +=py*i




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
                ax.add_patch(rect)

        plt.axis('equal')
        plt.axis('off')
        plt.show()

    def afficher_plateau_graphique_nx(self):
        G = nx.Graph()

        # Ajouter les villes comme nœuds
        for ville in self.villes:
            G.add_node(ville.nom, pos=(ville.coordonnees[0], ville.coordonnees[1]))  # (abcisse, ordonnée)

        # Ajouter les routes comme arêtes
        for route in self.routes:
            couleur_base = COULEURS_MATPLOTLIB.get(route.couleur, "gray")
            color = couleur_base if route.etat == "disponible" else "purple"
            style = "solid" if route.etat == "disponible" else "dotted"  # Style de ligne
            G.add_edge(route.Ville1.nom, route.Ville2.nom, color=color, style=style, weight=route.longueur)

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

    def __init__(self, Ville1, Ville2, couleur, longueur, double):
        self.Ville1 = Ville1
        self.Ville2 = Ville2
        self.longueur = longueur
        self.couleur = couleur
        self.double = double
        self.possesseur = None
        self.etat = "disponible"  # Par défaut, la route est disponible

    def capturer(self, joueur : Joueur):
        """Marque la route comme capturée par un joueur."""
        self.possesseur = joueur
        self.etat = "capturée"  # Change l'état de la route à "capturée"

#endregion
