import os
import matplotlib.pyplot as plt
import osmnx as ox
from matplotlib.lines import Line2D

def visualizar_grafo(engine, electrolineras, puntos_referencia):
    fig, ax = ox.plot_graph(
        engine.graph, show=False, close=False,
        bgcolor='#1a1a2e', node_color='#16213e', node_size=1,
        edge_color='#0f3460', edge_linewidth=0.5
    )
    for est in electrolineras:
        if 'node' not in est:
            continue
        d = engine.graph.nodes[est['node']]
        ax.scatter(d['x'], d['y'], c='#2ecc71', s=100, zorder=5, marker='^')
        ax.annotate(est['nombre'], (d['x'], d['y']),
                    fontsize=5, color='#2ecc71', ha='center', va='bottom')

    for p in puntos_referencia:
        if 'node' not in p:
            continue
        d = engine.graph.nodes[p['node']]
        ax.scatter(d['x'], d['y'], c='#3498db', s=70, zorder=5, marker='o')
        ax.annotate(p['nombre'], (d['x'], d['y']),
                    fontsize=4, color='#3498db', ha='center', va='bottom')

    plt.title("Red vial BGA — electrolineras y puntos de referencia",
              color='white', fontsize=11)
    leyenda = [
        Line2D([0],[0], marker='^', color='w', markerfacecolor='#2ecc71', markersize=9, label='Electrolinera'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor='#3498db', markersize=7, label='Punto referencia'),
    ]
    ax.legend(handles=leyenda, loc='upper right', facecolor='#1a1a2e', labelcolor='white')

    ruta = "data/grafo_red_vial.png"
    os.makedirs("data", exist_ok=True)
    plt.savefig(ruta, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print(f"visualización guardada: {ruta}")
    plt.show()

def visualizar_ruta(engine, ruta_nodos, origen="Origen", destino="Destino"):
    fig, ax = ox.plot_graph_route(
        engine.graph, ruta_nodos, show=False, close=False,
        route_color='#e74c3c', route_linewidth=3,
        bgcolor='#1a1a2e', node_size=0,
        edge_color='#0f3460', edge_linewidth=0.3
    )
    plt.title(f"ruta: {origen} → {destino}", color='white')
    ruta_img = f"data/ruta_{origen[:8]}_{destino[:8]}.png"
    os.makedirs("data", exist_ok=True)
    plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
    print(f"ruta guardada: {ruta_img}")
    plt.show()