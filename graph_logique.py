import matplotlib.pyplot as plt
import networkx as nx

# Création du graphe
G = nx.DiGraph()

# Nœuds
nodes = [
    "Début du tour",
    "Choix actions",
    "Piocher\ncarte wagon",
    "Carte\nlocomotive\npiochée\nvisible ?",
    "Fin du tour\n(locomotive)",
    "Peut piocher\n2e carte",
    "Fin du tour\n(2 cartes)",
    "Capturer une route",
    "Assez\nwagons/\nlocomotives ?",
    "Capturer route\ndisponible",
    "Retour\nchoix actions",
    "Pioche\nitinéraires\n(non dispo)",
    "Piocher 3 cartes",
    "Reposer\n0 à 2 cartes",
    "Vérifier\nnb wagons\nrestants",
    "Fin tour",
]
G.add_nodes_from(nodes)

# Arcs
edges = [
    ("Début du tour", "Choix actions"),
    ("Choix actions", "Piocher\ncarte wagon"),
    ("Choix actions", "Capturer une route"),
    ("Choix actions", "Pioche\nitinéraires\n(non dispo)"),
    ("Piocher\ncarte wagon", "Carte\nlocomotive\npiochée\nvisible ?"),
    ("Carte\nlocomotive\npiochée\nvisible ?", "Fin du tour\n(locomotive)", {"label": "Oui"}),
    ("Carte\nlocomotive\npiochée\nvisible ?", "Peut piocher\n2e carte", {"label": "Non"}),
    ("Peut piocher\n2e carte", "Fin du tour\n(2 cartes)"),
    ("Capturer une route", "Assez\nwagons/\nlocomotives ?"),
    ("Assez\nwagons/\nlocomotives ?", "Capturer route\ndisponible", {"label": "Oui"}),
    ("Assez\nwagons/\nlocomotives ?", "Retour\nchoix actions", {"label": "Non"}),
    ("Capturer route\ndisponible", "Vérifier\nnb wagons\nrestants"),
    ("Fin du tour\n(locomotive)", "Fin tour"),
    ("Fin du tour\n(2 cartes)", "Fin tour"),
    ("Retour\nchoix actions", "Choix actions"),
    ("Vérifier\nnb wagons\nrestants", "Fin tour"),
    ("Pioche\nitinéraires\n(non dispo)", "Piocher 3 cartes"),
    ("Piocher 3 cartes", "Reposer\n0 à 2 cartes"),
    ("Reposer\n0 à 2 cartes", "Fin tour"),
]

for edge in edges:
    if len(edge) == 3:
        G.add_edge(edge[0], edge[1], label=edge[2]["label"])
    else:
        G.add_edge(edge[0], edge[1])

# Positionnement manuel des nœuds
pos = {
    "Début du tour": (0, 6),
    "Choix actions": (0, 5),
    "Piocher\ncarte wagon": (-4, 4),
    "Carte\nlocomotive\npiochée\nvisible ?": (-4, 3),
    "Fin du tour\n(locomotive)": (-3, 2),
    "Peut piocher\n2e carte": (-4, 2),
    "Fin du tour\n(2 cartes)": (-4, 1),
    "Capturer une route": (0, 4),
    "Assez\nwagons/\nlocomotives ?": (0, 3),
    "Capturer route\ndisponible": (0, 2),
    "Retour\nchoix actions": (-1, 3),
    "Pioche\nitinéraires\n(non dispo)": (4, 4),
    "Piocher 3 cartes": (4, 3),
    "Reposer\n0 à 2 cartes": (4, 2),
    "Vérifier\nnb wagons\nrestants": (0, 1),
    "Fin tour": (0, 0),
}

# Couleurs des nœuds
color_map = {
    "Piocher\ncarte wagon": "skyblue",
    "Carte\nlocomotive\npiochée\nvisible ?": "skyblue",
    "Peut piocher\n2e carte": "skyblue",
    "Fin du tour\n(locomotive)": "skyblue",
    "Fin du tour\n(2 cartes)": "skyblue",
    "Capturer une route": "lightgreen",
    "Assez\nwagons/\nlocomotives ?": "lightgreen",
    "Capturer route\ndisponible": "lightgreen",
    "Retour\nchoix actions": "lightgreen",
    "Pioche\nitinéraires\n(non dispo)": "violet",
    "Piocher 3 cartes": "violet",
    "Reposer\n0 à 2 cartes": "violet",
    "Choix actions": "gold",
    "Début du tour": "orange",
    "Vérifier\nnb wagons\nrestants": "salmon",
    "Fin tour": "salmon",
}
node_colors = [color_map.get(node, "lightgray") for node in G.nodes()]

# Tracé
plt.figure(figsize=(18, 12))
ax = plt.gca()
nx.draw_networkx_nodes(G, pos, node_size=5000, node_color=node_colors, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)

# Tracer les arêtes avec des flèches droites
for u, v in G.edges():
    ax.annotate("",
                xy=pos[v], xycoords='data',
                xytext=pos[u], textcoords='data',
                arrowprops=dict(arrowstyle="-|>", color="gray", shrinkA=25, shrinkB=25))

# Labels des flèches
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True) if 'label' in d}
for (u, v), label in edge_labels.items():
    if label:
        x_src, y_src = pos[u]
        x_dst, y_dst = pos[v]
        x_mid, y_mid = (x_src + x_dst) / 2, (y_src + y_dst) / 2
        ax.text(x_mid, y_mid+0.07, label, fontsize=9, color='red', ha='center')

plt.title("Diagramme logique d'un tour (Les Aventuriers du Rail)", fontsize=16, fontweight='bold')
plt.axis('off')
plt.show()
