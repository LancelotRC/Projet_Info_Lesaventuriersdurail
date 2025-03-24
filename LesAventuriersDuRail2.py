import networkx as nx
import matplotlib.pyplot as plt



# Classe principale regroupant tout
class Table:
    def __init__(self, joueurs, plateau, pioche):
        self.joueurs = joueurs  # Liste des joueurs
        self.plateau = plateau  # Plateau de jeu
        self.pioche = pioche  # Pioche des cartes wagon


# Classe représentant un joueur
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.cartes_wagon = []  # Cartes wagon en main
        self.cartes_defi = []  # Cartes destination/objectifs
        self.wagons_restants = 45  # Wagons restants au début
        self.routes_prises = [] # liste des itinéraires pris par le joueur
        
    def calculer_points_routes(self):
        points = 0
        for route in self.routes_prises:
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
    
    def villes_sont_elles_reliees(): # algorithme de recherche de chemin entre deux ville, ça servira pour savoir si la carte défi a été accompli
        
    
    
    def calculer_points_destinations(self):
        points = 0
        for destination in self.cartes_defi:
            if self.sont_villes_reliees(destination.ville_depart, destination.ville_arrivee):
                points += destination.points
            else:
                points -= destination.points
        return points


# Classe représentant une carte défi (destination)
class CarteDefi:
    def __init__(self, ville_depart, ville_arrivee, points):
        self.ville_depart = ville_depart
        self.ville_arrivee = ville_arrivee
        self.points = points
        self.possesseur = None  # Joueur possédant cette carte (None si pas encore attribuée)


# Classe représentant une pioche (cartes wagons ou cartes défi)
class Pioche:
    def __init__(self, cartes):
        self.cartes = cartes

    def piocher(self):
        if self.cartes:
            return self.cartes.pop()
        else:
            return None


# Classe représentant le plateau de jeu
class Plateau:
    def __init__(self, villes, itineraires):
        self.villes = villes  # Liste des villes
        self.itineraires = itineraires  # Liste des itinéraires (arêtes)
    
    def ajouter_ville(self, ville):
        """Ajoute une ville au plateau."""
        self.villes.append(ville)

    def ajouter_itineraire(self, itineraire):
        """Ajoute un itinéraire au plateau."""
        self.itineraires.append(itineraire)

    def get_itineraires_adjacents(self, ville):
        """Retourne tous les itinéraires adjacents à une ville donnée."""
        return [itineraire for itineraire in self.itineraires 
                if ville in (itineraire.ville1, itineraire.ville2)]

    def est_itineraire_libre(self, itineraire):
        """Vérifie si un itinéraire est libre (non pris par un joueur)."""
        return itineraire.possesseur is None


# Classe représentant un itinéraire entre deux villes
class Itineraire:
    def __init__(self, ville1, ville2, longueur, couleur=None):
        self.ville1 = ville1
        self.ville2 = ville2
        self.longueur = longueur
        self.couleur = couleur  # Couleur nécessaire pour l'itinéraire (None si gris)
        self.possesseur = None  # Joueur qui possède l'itinéraire, None par défaut


# Classe représentant une ville
class Ville:
    def __init__(self, nom, coordonnees=None):
        self.nom = nom
        self.coordonnees = coordonnees  # Coordonnées optionnelles (x, y) pour affichage graphique



# Créer les villes
ville1 = Ville("New York")
ville2 = Ville("Los Angeles")
ville3 = Ville("Chicago")

# Créer les itinéraires
itineraire1 = Itineraire(ville1, ville2, longueur=3, couleur="r")
itineraire2 = Itineraire(ville2, ville3, longueur=2, couleur="b")
itineraire3 = Itineraire(ville1, ville3, longueur=4, couleur="k")  # Itinéraire gris

# Créer le plateau
plateau = Plateau(villes=[ville1, ville2, ville3], itineraires=[itineraire1, itineraire2, itineraire3])



def afficher_graphe(plateau):
    # Créer un graphe NetworkX
    G = nx.Graph()

    # Ajouter les villes (nœuds)
    for ville in plateau.villes:
        G.add_node(ville.nom)

    
    # Ajouter les itinéraires (arêtes)
    for itineraire in plateau.itineraires:
        G.add_edge(itineraire.ville1.nom, itineraire.ville2.nom, 
                   couleur=itineraire.couleur, longueur=itineraire.longueur)

    # Dessiner le graphe
    pos = nx.spring_layout(G)  # Positionnement des nœuds
    couleurs = [G[u][v]['couleur'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, edge_color=couleurs, width=2, node_size=2000, node_color='lightblue')
    plt.show()

# Afficher le graphe
afficher_graphe(plateau)


