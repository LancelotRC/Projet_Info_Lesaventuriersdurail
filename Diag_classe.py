import networkx as nx
import matplotlib.pyplot as plt

# Création du graphe représentant les classes
G = nx.DiGraph()

# Ajout des classes (noeuds)
classes = ["Table", "Joueur", "CarteDefi", "CarteWagon",
           "Pioche", "PiocheWagon", "PiocheItineraire",
           "Plateau", "Itineraire", "Ville"]

G.add_nodes_from(classes)

# Ajout des relations d'héritage (arêtes)
heritage = [("Pioche", "PiocheWagon"),
            ("Pioche", "PiocheItineraire")]

# Ajout des relations de composition (arêtes)
composition = [("Table", "Joueur"),
               ("Table", "Plateau"),
               ("Table", "PiocheWagon"),
               ("Table", "PiocheItineraire"),
               ("Plateau", "Ville"),
               ("Plateau", "Itineraire"),
               ("Joueur", "CarteWagon"),
               ("Joueur", "CarteDefi"),
               ("Itineraire", "Ville")]

# Ajout des arêtes au graphe
G.add_edges_from(heritage + composition)

# Définition du layout du graphe
pos = nx.spring_layout(G)

# Dessin du graphe
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2500, font_size=10, font_weight='bold', arrows=True)

# Ajout des étiquettes spécifiques pour les relations
edge_labels = {}
for edge in heritage:
    edge_labels[edge] = 'hérite'
for edge in composition:
    edge_labels[edge] = 'contient'

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

# Afficher le graphe
plt.title("Diagramme de Classes - Aventuriers du Rail")
plt.axis('off')
plt.show()
