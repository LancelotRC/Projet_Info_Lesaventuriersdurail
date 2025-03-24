import random
import networkx as nx
import matplotlib.pyplot as plt

# definition des données pour le jeu version USA

# Définition des villes du plateau USA
VILLES_USA = {
    "Atlanta": (33.75, -84.39),
    "Boston": (42.35, -71.05),
    "Calgary": (51.05, -114.05),
    "Charleston": (32.78, -79.93),
    "Chicago": (41.83, -87.62),
    "Dallas": (32.77, -96.79),
    "Denver": (39.74, -104.99),
    "Duluth": (46.78, -92.11),
    "El Paso": (31.76, -106.49),
    "Helena": (46.59, -112.02),
    "Houston": (29.76, -95.36),
    "Kansas City": (39.08, -94.58),
    "Las Vegas": (36.17, -115.14),
    "Little Rock": (34.74, -92.33),
    "Los Angeles": (34.05, -118.24),
    "Miami": (25.78, -80.21),
    "Montreal": (45.50, -73.56),
    "Nashville": (36.16, -86.78),
    "New Orleans": (29.95, -90.07),
    "New York": (40.71, -74.01),
    "Oklahoma City": (35.47, -97.51),
    "Omaha": (41.26, -95.94),
    "Phoenix": (33.45, -112.07),
    "Pittsburgh": (40.44, -79.99),
    "Portland": (45.52, -122.68),
    "Raleigh": (35.78, -78.64),
    "Saint Louis": (38.63, -90.20),
    "Salt Lake City": (40.76, -111.89),
    "San Francisco": (37.77, -122.42),
    "Santa Fe": (35.68, -105.94),
    "Seattle": (47.61, -122.33),
    "Toronto": (43.65, -79.38),
    "Vancouver": (49.28, -123.12),
    "Washington": (38.90, -77.04),
    "Winnipeg": (49.90, -97.14)
}

# Définition des routes (Ville1, Ville2, couleur, longueur)
ROUTES_USA = [
    ("Atlanta", "Nashville", "gris", 1), ("Atlanta", "Raleigh", "gris", 2), ("Atlanta", "Charleston", "gris", 2),
    ("Atlanta", "New Orleans", "orange", 4), ("Boston", "Montreal", "gris", 2), ("Boston", "New York", "jaune", 2),
    ("Calgary", "Vancouver", "gris", 3), ("Calgary", "Seattle", "gris", 4), ("Calgary", "Helena", "gris", 4),
    ("Charleston", "Raleigh", "gris", 2), ("Chicago", "Saint Louis", "vert", 2), ("Chicago", "Pittsburgh", "orange", 3),
    ("Chicago", "Duluth", "rouge", 3), ("Dallas", "Houston", "gris", 1), ("Dallas", "Oklahoma City", "gris", 2),
    ("Dallas", "Little Rock", "gris", 2), ("Denver", "Santa Fe", "gris", 2), ("Denver", "Oklahoma City", "rouge", 4),
    ("Denver", "Salt Lake City", "rouge", 3), ("El Paso", "Santa Fe", "gris", 2), ("El Paso", "Phoenix", "gris", 3),
    ("Las Vegas", "Los Angeles", "gris", 2), ("Los Angeles", "Phoenix", "jaune", 3),
    ("Los Angeles", "San Francisco", "jaune", 3), ("Los Angeles", "El Paso", "noir", 6), ("Miami", "New Orleans", "rouge", 6),
    ("Montreal", "Toronto", "gris", 3), ("New Orleans", "Houston", "gris", 2), ("New York", "Washington", "noir", 2),
    ("Pittsburgh", "Raleigh", "gris", 2), ("Salt Lake City", "San Francisco", "orange", 5), ("Seattle", "Portland", "gris", 1),
    ("Seattle", "Helena", "jaune", 6), ("Toronto", "Pittsburgh", "gris", 2), ("Vancouver", "Seattle", "gris", 1),
    ("Washington", "Raleigh", "gris", 2)
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


# Classe principale regroupant tout
class Table:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.plateau = Plateau(VILLES_USA, ROUTES_USA)
        self.pioche_wagon = PiocheWagon([CarteWagon(c) for c in ["rouge", "bleu", "vert", "jaune", "noir", "blanc", "orange", "violet"] * 12 + ["locomotive"] * 14])
        self.pioche_itineraire = PiocheItineraire([CarteItineraire(v1, v2, p) for v1, v2, p in CARTES_DESTINATION_USA])

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
            print(f"Wagons restants : {joueur.wagons_restants}")
            print(f"Cartes wagon en main : {[c.couleur for c in joueur.cartes_wagon]}")
            print(f"Cartes destination : {[f'{c.ville_depart} → {c.ville_arrivee}' for c in joueur.cartes_defi]}")

            print("1. Piocher une carte wagon")
            print("2. Capturer une route")
            print("3. Piocher des cartes destination")
            print("4. Quitter le jeu")

            choix = input("Choisissez une action (1, 2, 3, 4) : ")

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
                print("Fin de la partie. Merci d'avoir joué !")
                exit()
            else:
                print("❌ Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")

    def capturer_route(self, joueur):
        """Permet à un joueur de capturer une route en défaussant les cartes nécessaires"""
        print("\nRoutes disponibles :")
        routes_disponibles = [route for route in self.plateau.routes if route.dispo is None]

        if not routes_disponibles:
            print("Aucune route n'est disponible à capturer.")
            return

        # Afficher les routes disponibles
        for i, route in enumerate(routes_disponibles):
            print(f"{i}: {route.Ville1} → {route.Ville2} ({route.longueur} cases, couleur : {route.couleur})")

        choix = int(input("Choisissez une route à capturer (numéro) : "))

        if choix < 0 or choix >= len(routes_disponibles):
            print("Choix invalide.")
            return

        route_choisie = routes_disponibles[choix]

        # Vérifier que le joueur a assez de wagons
        if joueur.wagons_restants < route_choisie.longueur:
            print("Vous n'avez pas assez de wagons pour capturer cette route.")
            return

        # Vérifier que le joueur a les bonnes cartes wagon
        if not joueur.verifier_cartes_wagon(route_choisie):
            print("Vous n'avez pas les cartes nécessaires pour capturer cette route.")
            return

        # Défausser les cartes utilisées
        self.defausser_cartes_wagon(joueur, route_choisie)

        # Marquer la route comme occupée
        route_choisie.dispo = False
        route_choisie.possesseur = joueur
        joueur.wagons_restants -= route_choisie.longueur

        print(f"{joueur.nom} a capturé la route {route_choisie.Ville1} → {route_choisie.Ville2}!")

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
        cartes_piochees = []

        # Affichage des cartes visibles
        print("\nCartes disponibles :")
        for i, carte in enumerate(self.pioche_wagon.visible):
            print(f"{carte.couleur}")

        # Premier tirage
        carte1, pioche = self.choisir_carte_wagon()
        if not carte1:
            print("Aucune carte n'a pu être piochée.")
            return
        joueur.cartes_wagon.append(carte1)
        print(f"{joueur.nom}, vous avez choisi la carte {carte1.couleur}")

        # Vérifier si c'était une locomotive → Pas de deuxième pioche
        if carte1.is_locomotive and pioche == 1:
            print(f"{joueur.nom} a pioché une locomotive et ne peut pas prendre de deuxième carte. Fin du tour.")
            return  # ✅ Arrêt immédiat

        # Deuxième tirage
        carte2 = self.choisir_carte_wagon(interdit_locomotive=True)[0]
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
                    else:
                        self.pioche_wagon.remelanger_si_vide()
                        self.pioche_wagon.visible.append(self.pioche_wagon.piocher_cachee())

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


# Classe représentant un joueur
class Joueur:
    def __init__(self, nom, couleur):
        self.nom = nom
        self.couleur = couleur
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

# Classe représentant les cartes wagon
class CarteWagon:
    def __init__(self, couleur):
        self.couleur = couleur
        self.is_locomotive = (couleur == "locomotive")  # Ajout d’un flag pour éviter des vérifications de texte

    def __str__(self):
        return f"Carte Wagon ({self.couleur})"

# Classe représentant les cartes itinéraire
class CarteItineraire:
    def __init__(self, ville_depart, ville_arrivee, points):
        self.ville_depart = ville_depart
        self.ville_arrivee = ville_arrivee
        self.points = points
        self.possesseur = None  # Joueur possédant cette carte

    def __str__(self):
        return f"{self.ville_depart} → {self.ville_arrivee} ({self.points} points)"

# Classe représentant la pioche des cartes Wagon
class PiocheWagon:
    def __init__(self, cartes):
        self.pioche = cartes  # Liste des cartes wagon
        random.shuffle(self.pioche)
        self.visible = [self.pioche.pop() for _ in range(5)]  # 5 cartes visibles
        self.defausse = []

    def piocher_visible(self, index):
        """Pioche une carte visible et la remplace par une carte de la pioche cachée."""
        if 0 <= index < len(self.visible):
            carte = self.visible.pop(index)
            self.remelanger_si_vide()  # Vérifier et mélanger si nécessaire
            if self.pioche:
                self.visible.append(self.pioche.pop())
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
        """Vérifie que la pioche visible ne contient pas 5 locomotives.
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
class PiocheItineraire:
    def __init__(self, cartes):
        self.pioche = cartes  # Liste des cartes destination
        random.shuffle(self.pioche)

    def piocher(self):
        """Pioche trois cartes destination."""
        return [self.pioche.pop() for _ in range(min(3, len(self.pioche)))]

    def replacer_en_bas(self, cartes):
        """Replace les cartes non gardées en bas de la pioche."""
        self.pioche = cartes + self.pioche

# Classe représentant le plateau de jeu (toutes les villes et les routes)
class Plateau:
    def __init__(self, dico_ville, dico_route):
        self.villes = [Ville(nom, coordonnees=dico_ville[nom]) for nom in dico_ville]
        self.routes = [Route(V1, V2, couleur, longueur) for V1, V2, couleur, longueur in dico_route]  # ✅ Convertit en objets Route
        self.afficher_plateau_graphique()

    def afficher_plateau_graphique(self):
        G = nx.Graph()

        # Ajouter les villes comme nœuds
        for ville in self.villes:
            G.add_node(ville.nom, pos=(ville.coordonnees[1], ville.coordonnees[0]))  # (longitude, latitude)

        # Ajouter les routes comme arêtes
        for route in self.routes:
            G.add_edge(route.Ville1, route.Ville2, color=route.couleur, weight=route.longueur)

        # Préparer l'affichage
        pos = nx.get_node_attributes(G, 'pos')
        couleurs = [G[u][v]['color'] for u, v in G.edges()]
        poids = [G[u][v]['weight'] for u, v in G.edges()]

        # Afficher
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, edge_color=couleurs, width=poids, node_size=500, font_size=8)
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
        self.dispo = None #(True si dispo False si occupée)
        self.possesseur = None



## lancer le jeu

## ajouter le joueur aléatoire
## comptage des points
## graphique pour le plateau
