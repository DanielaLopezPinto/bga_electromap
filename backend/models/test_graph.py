from graph_engine import GraphEngine
from data import electrolineras, puntos_referencia
import osmnx as ox

engine = GraphEngine()
engine.load_map()

engine.energy_weight()
engine.assign_nodes(electrolineras)
engine.assign_nodes(puntos_referencia)

import networkx as nx

origen = puntos_referencia[0]
destino = puntos_referencia[1]

origin_node = origen["node"]
target_node = destino["node"]

# Ruta más corta
ruta_dist = nx.shortest_path(
    engine.graph,
    origin_node,
    target_node,
    weight="length"
)

# Ruta más eficiente
ruta_energy = nx.shortest_path(
    engine.graph,
    origin_node,
    target_node,
    weight="consumo"
)

dist1 = engine.get_route_distance(ruta_dist)
dist2 = engine.get_route_distance(ruta_energy)

cons1 = engine.get_route_consumption(ruta_dist)
cons2 = engine.get_route_consumption(ruta_energy)

print("\nRuta más corta")
print("Distancia:", dist1)
print("Consumo:", cons1)

print("\nRuta más eficiente")
print("Distancia:", dist2)
print("Consumo:", cons2)