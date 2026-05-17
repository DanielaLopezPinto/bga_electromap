import osmnx as ox
import networkx as nx
import os

CACHE_PATH = "data/graph_cache.graphml"

class GraphEngine:
    def __init__(self):
        self.graph = None
        self.electrolinera_nodes = []
        self.referencia_nodes = []

    def load_map(self, lugar="Bucaramanga, Santander, Colombia", usar_cache=True):
        if usar_cache and os.path.exists(CACHE_PATH):
            print("cargando mapa desde caché local...")
            self.graph = ox.load_graphml(CACHE_PATH)
        else:
            print(f"descargando mapa desde OpenStreetMap: '{lugar}'...")
            self.graph = ox.graph_from_place(lugar, network_type="drive", retain_all=False)
            os.makedirs("data", exist_ok=True)
            ox.save_graphml(self.graph, CACHE_PATH)
            print(f"mapa en caché: {CACHE_PATH}")
        print(f"nodos: {len(self.graph.nodes)} | Aristas: {len(self.graph.edges)}")
        return self.graph

    def energy_weight(self, consumo_base_kwh_km=0.15):
        for u, v, data in self.graph.edges(data=True):
            longitud = data.get('length', 50)
            pendiente = data.get('grade', 0.0)
            factor = 1.0 + max(0, pendiente) * 2.0
            data['consumo'] = (longitud / 1000) * consumo_base_kwh_km * factor
        print("pesos de consumo energético asignados a aristas")

    def assign_nodes(self, lugares):
        for lugar in lugares:
            nodo = ox.distance.nearest_nodes(self.graph, lugar['lon'], lugar['lat'])
            lugar['node'] = nodo
        return lugares

    def get_route_distance(self, ruta):
        distancia = 0
        for i in range(len(ruta) - 1):
            datos = self.graph.get_edge_data(ruta[i], ruta[i + 1])
            if datos:
                if isinstance(datos, dict) and 0 in datos:
                    datos = datos[0]
                distancia += datos.get('length', 50)
        return round(distancia / 1000, 3)

    def get_route_consumption(self, ruta):
        consumo = 0
        for i in range(len(ruta) - 1):
            datos = self.graph.get_edge_data(ruta[i], ruta[i + 1])
            if datos:
                if isinstance(datos, dict) and 0 in datos:
                    datos = datos[0]
                consumo += datos.get('consumo', datos.get('length', 50) / 1000 * 0.15)
        return round(consumo, 4)