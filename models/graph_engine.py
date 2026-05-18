import random
import osmnx as ox
import networkx as nx
from data import electrolineras

class GraphEngine:
    def __init__(self):
        #sefl.city define la ciudad que se descargará desde OpenStreetMap
        self.city = "Bucaramanga, Colombia"
        # se almacena el grafo
        self.graph = None

# Carga el mapa de la ciudad y lo convierte en el grafo 
    def load_map(self):
        print(f"Cargando mapa de {self.city}...")
        self.graph = ox.graph_from_place(self.city, network_type="drive") 
        #Solo incluye calles transitables por vehículos
        self.graph = ox.add_edge_speeds(self.graph)
        #Añade velocidad estimada a cada calle.
        self.graph = ox.add_edge_travel_times(self.graph)
        
        return self.graph
    
# OSMnx descarga:
# calles,
# intersecciones,
# sentidos de vías,
# conexiones.
# Y crea un grafo donde:
# nodos = intersecciones,
# aristas = calles

# Convierte las ubicaciones (coordenadas) a nodos
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
    
# Calcular la distancia total de una ruta
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
        # recorre todas las estaciones
        for e in electrolineras:
            try:
                # calcula la ruta hacia cada una
                route = nx.shortest_path(
                    self.graph,
                    current_node,
                    e["node"],
                    weight="length"
                )

                dist = self.get_route_distance(route)
                #calcula la distacia y escoge la menor
                if dist < min_dist:
                    min_dist = dist
                    best_station = e
                    best_route = route

            except nx.NetworkXNoPath:
                continue

        return best_station, best_route, min_dist
    # devuelve, la ruta, la distancia y la estación más cercana
    
    def energy_weight(self, consumo_por_km=0.2):
        for u, v, k, data in self.graph.edges(keys=True, data=True):

            distancia_km = data["length"] / 1000
            consumo = distancia_km * consumo_por_km
            
# Se usa para generar variaciones aleatorias en el consumo energético:
# tráfico, pendientes, frenadas, condiciones climáticas, etc.
            factor = random.uniform(1, 1.5) 
            data["consumo"] = consumo * factor

# Suma todo el consumo de una ruta para estimar el consumo total del viaje
    def get_route_consumption(self, route):
        consumo = 0

        for i in range(len(route) - 1):
            u = route[i]
            v = route[i + 1]

            edge_data = self.graph.get_edge_data(u, v)[0]
            consumo += edge_data.get("consumo", 0)
        return consumo

# Encuentra la ruta de menor consumo energético
    def get_most_efficient_path(self, origin_node, target_node):
        if not self.graph:
            self.load_map()
        return nx.shortest_path(self.graph, origin_node, target_node, weight="consumo")
        
# Encuentra la ruta de menor tiempo de viaje, algo un poco mas realista
# que una ruta matematicamente mas corta
    def get_shortest_path(self, origin_node, target_node):
        if not self.graph:
            self.load_map()
        return nx.shortest_path(self.graph, origin_node, target_node, weight="travel_time")
    
    