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

# Relations
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
    ("Joueur", "CarteWagon"), ("Joueur", "CarteItineraire")
]
G.add_edges_from(heritage + composition)

# Positions manuelles
pos = {
    "Table": (0, 0),
    "Plateau": (-2.5, -1), "Ville": (-3.5, -2), "Route": (-1.5, -2),
    "Joueur": (2.5, -1), "CarteWagon": (2, -2.2), "CarteItineraire": (3, -2.2),
    "Carte": (2.5, -3.2),
    "PiocheWagon": (-1, 1), "PiocheItineraire": (1, 1), "Pioche": (0, 2)
}

# Couleurs
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
        node_colors.append("gold")
    elif node == "Joueur":
        node_colors.append("orange")
    elif node == "Table":
        node_colors.append("salmon")
    else:
        node_colors.append("lightyellow")

# Edge labels
edge_labels = {edge: "hérite" for edge in heritage}
edge_labels.update({edge: "contient" for edge in composition})

# Tracé
plt.figure(figsize=(15, 13))
ax = plt.gca()

# Tracer les arêtes avec style conditionnel et labels intégrés
for u, v in G.edges():
    # Déterminer si la flèche doit être courbée
    if (u, v) in [("PiocheWagon", "CarteWagon"), ("PiocheItineraire", "CarteItineraire")]:
        style = "arc3,rad=0.3"
    else:
        style = "arc3,rad=0"

    # Tracer la flèche
    ax.annotate("",
                xy=pos[v], xycoords='data',
                xytext=pos[u], textcoords='data',
                arrowprops=dict(arrowstyle='-|>',
                                color='gray',
                                shrinkA=15, shrinkB=15,
                                connectionstyle=style))

    # Tracer le label
    label = edge_labels.get((u, v), "")
    if label:
        x_src, y_src = pos[u]
        x_dst, y_dst = pos[v]
        x_mid, y_mid = (x_src + x_dst) / 2, (y_src + y_dst) / 2
        if (u, v) == ("PiocheWagon", "CarteWagon"):
            ax.text(x_mid - 0.5, y_mid - 0.6, label, fontsize=9, color='red', ha='center')
        elif (u, v) == ("PiocheItineraire", "CarteItineraire"):
            ax.text(x_mid - 0.5, y_mid - 0.6, label, fontsize=9, color='red', ha='center')
        elif (u, v) == ("Table", "Joueur"):
            ax.text(x_mid*0.5, y_mid*0.5 + 0.1 , label, fontsize=9, color='red', ha='center')
        elif (u, v) == ("Table", "Plateau"):
            ax.text(x_mid * 1.5, y_mid * 1.5 + 0.1, label, fontsize=9, color='red', ha='center')
        else:
            ax.text(x_mid, y_mid + 0.1, label, fontsize=9, color='red', ha='center')

# Tracer les nœuds et labels
nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=node_colors, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)

plt.title("Diagramme de classes – flèches courbes et labels intégrés", fontsize=14, fontweight='bold')
plt.axis('off')
plt.show()
