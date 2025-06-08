import matplotlib.pyplot as plt
import networkx as nx

# Création du graphe orienté
G = nx.DiGraph()

# Liste des classes
classes = [
    "Table", "Joueur", "Carte", "CarteWagon", "CarteItineraire",
    "Pioche", "PiocheWagon", "PiocheItineraire", "Plateau", "Route", "Ville"
]
G.add_nodes_from(classes)

# Relations d'héritage et de composition
heritage = [
    ("PiocheWagon", "Pioche"),
    ("PiocheItineraire", "Pioche"),
    ("CarteWagon", "Carte"),
    ("CarteItineraire", "Carte")
]
composition = [
    ("Table", "Joueur"), ("Table", "Plateau"),
    ("Table", "PiocheWagon"), ("Table", "PiocheItineraire"),
    ("Plateau", "Ville"), ("Plateau", "Route"),
    ("PiocheWagon", "CarteWagon"), ("PiocheItineraire", "CarteItineraire"),
    ("Joueur", "CarteWagon"), ("Joueur", "CarteItineraire"),
    ("Joueur", "Route")  # 🔁 Ajout : lien capture
]
G.add_edges_from(heritage + composition)

# Positionnement
pos = {
    "Carte": (2, 2.5), "Pioche": (0, 2.5),
    "CarteWagon": (2.5, 1.5), "CarteItineraire": (1.5, 1.5),
    "PiocheWagon": (-0.5, 1.5), "PiocheItineraire": (0.5, 1.5),
    "Table": (1, 0),
    "Plateau": (0, -1), "Ville": (-0.5, -2), "Route": (0.5, -2),
    "Joueur": (2, -1),
}

# Couleurs des nœuds
node_colors = []
for node in G.nodes():
    if node == "Pioche":
        node_colors.append("violet")
    elif node == "Carte":
        node_colors.append("lightblue")
    elif node.startswith("Pioche"):
        node_colors.append("violet")
    elif node.startswith("Carte"):
        node_colors.append("skyblue")
    elif node in ["Ville", "Route"]:
        node_colors.append("lightgreen")
    elif node == "Plateau":
        node_colors.append("lightgreen")
    elif node == "Joueur":
        node_colors.append("orange")
    elif node == "Table":
        node_colors.append("salmon")
    else:
        node_colors.append("lightyellow")

# Labels des arêtes
edge_labels = {edge: "hérite" for edge in heritage}
edge_labels.update({edge: "contient" for edge in composition})
edge_labels[("Joueur", "Route")] = "capture"  # Etiquette spéciale

# Tracé
plt.figure(figsize=(15, 13))
ax = plt.gca()

# Catégories pour les couleurs de flèches
pioche_nodes = {"Pioche", "PiocheWagon", "PiocheItineraire"}
carte_nodes = {"Carte", "CarteWagon", "CarteItineraire"}
plateau_nodes = {"Plateau", "Ville", "Route"}

for u, v in G.edges():
    style = "arc3,rad=0.3" if (u, v) in [
        ("PiocheWagon", "CarteWagon"),
        ("PiocheItineraire", "CarteItineraire")
    ] else "arc3,rad=0"

    # couleur selon branche
    if {u, v} <= pioche_nodes:
        edge_color = "purple"
    elif {u, v} <= carte_nodes:
        edge_color = "deepskyblue"
    elif {u, v} <= plateau_nodes:
        edge_color = "green"
    elif (u, v) in heritage:
        edge_color = "black"
    else:
        edge_color = "gray"

    ax.annotate("",
                xy=pos[v], xycoords='data',
                xytext=pos[u], textcoords='data',
                arrowprops=dict(arrowstyle='-|>',
                                color=edge_color,
                                shrinkA=15, shrinkB=15,
                                connectionstyle=style))

    label = edge_labels.get((u, v), "")
    if label:
        x_src, y_src = pos[u]
        x_dst, y_dst = pos[v]
        x_mid, y_mid = (x_src + x_dst) / 2, (y_src + y_dst) / 2

        # Placement spécial pour les arêtes incurvées
        if (u, v) == ("PiocheWagon", "CarteWagon"):
            ax.text(x_mid + 0.025, y_mid - 0.2, label, fontsize=9, color='red', ha='center')
        elif (u, v) == ("PiocheItineraire", "CarteItineraire"):
            ax.text(x_mid + 0.25, y_mid - 0.7, label, fontsize=9, color='red', ha='center')
        else:
            ax.text(x_mid, y_mid + 0.1, label, fontsize=9, color='red', ha='center')

# Nœuds et étiquettes
nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=node_colors, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)

plt.title("Diagramme de classes – héritage vs composition", fontsize=14, fontweight='bold')
plt.axis('off')
plt.show()

