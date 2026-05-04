import random

import osmnx as ox
import networkx as nx
from data import electrolineras

class GraphEngine:
    def __init__(self):
        self.city = "Bucaramanga, Colombia"
        self.graph = None

# Carga el mapa de la ciudad y prepara el grafo 
    def load_map(self):
        print(f"Cargando mapa de {self.city}...")
        self.graph = ox.graph_from_place(self.city, network_type="drive") 
        
        self.graph = ox.add_edge_speeds(self.graph)
        self.graph = ox.add_edge_travel_times(self.graph)
        
        return self.graph

# Convertir ubicaciones a nodos
    def assign_nodes(self, locations):
        for loc in locations:
            node = ox.nearest_nodes(self.graph, loc["lon"], loc["lat"])
            loc["node"] = node

# Etiqueta las electrolineras en el grafo para facilitar su identificación            
    def tag_electrolineras(self, electrolineras):
        for e in electrolineras:
            node = e["node"]
            self.graph.nodes[node]["tipo"] = "electrolinera"
            self.graph.nodes[node]["nombre"] = e["nombre"]

# Obtiene la ruta más corta entre dos coordenadas (latitud y longitud)
    def get_route_by_coords(self, lat1, lon1, lat2, lon2):
        origin = ox.nearest_nodes(self.graph, lon1, lat1)
        target = ox.nearest_nodes(self.graph, lon2, lat2)

        route = nx.shortest_path(
            self.graph,
            origin,
            target,
            weight="length"
        )

        return route
    
# Calcular la distancia de una ruta
    def get_route_distance(self, route):
        distance = 0

        for i in range(len(route) - 1):
            u = route[i]
            v = route[i + 1]

            edge_data = self.graph.get_edge_data(u, v)[0]
            distance += edge_data["length"]

        return distance

# Encuentra la electrolinera mas cercana 
    def nearest_charging_station(self, current_node, electrolineras):
        min_dist = float("inf")
        best_station = None
        best_route = None

        for e in electrolineras:
            try:
                route = nx.shortest_path(
                    self.graph,
                    current_node,
                    e["node"],
                    weight="length"
                )

                dist = self.get_route_distance(route)

                if dist < min_dist:
                    min_dist = dist
                    best_station = e
                    best_route = route

            except:
                continue

        return best_station, best_route, min_dist
    
    def energy_weight(self, consumo_por_km=0.2):
        for u, v, k, data in self.graph.edges(keys=True, data=True):

            distancia_km = data["length"] / 1000

            consumo = distancia_km * consumo_por_km

            factor = random.uniform(1, 1.5)
            data["consumo"] = consumo * factor

    def get_route_consumption(self, route):
        consumo = 0

        for i in range(len(route) - 1):
            u = route[i]
            v = route[i + 1]

            edge_data = self.graph.get_edge_data(u, v)[0]

            
            consumo += edge_data.get("consumo", 0)
        return consumo
    
    def get_shortest_path(self, origin_node, target_node):
        if not self.graph:
            self.load_map()
        return nx.shortest_path(self.graph, origin_node, target_node, weight="length")