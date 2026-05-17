import random
from datetime import datetime
from simulation.vehicle_model import Vehiculo
from graph.nearest_station import encontrar_mas_cercana
from graph.routing import dijkstra
from data.vehicles import obtener_todos

class Simulator:
    def __init__(self, engine):
        self.engine    = engine
        self.logs      = []
        self.vehiculos = []

    def inicializar_vehiculos(self):
        self.vehiculos = [Vehiculo(v) for v in obtener_todos()]
        print(f"[+] {len(self.vehiculos)} vehículos inicializados desde la base de datos.")

    def run(self, n_recorridos=150):
        # CORREGIDO: Limpieza y reinicio de estado al arrancar la simulación
        self.logs = [] 
        self.inicializar_vehiculos() 

        electrolineras = self.engine.electrolinera_nodes
        referencias    = [r for r in self.engine.referencia_nodes if 'node' in r]

        if len(referencias) < 2:
            print("!faltan nodos de referencia asignados.")
            return self.logs

        print(f"\n iniciando {n_recorridos} recorridos aleatorios en el mapa...\n")

        contador = 0
        while contador < n_recorridos:
            vehiculo    = random.choice(self.vehiculos)
            origen_ref  = random.choice(referencias)
            opciones    = [r for r in referencias if r['node'] != origen_ref['node']]
            destino_ref = random.choice(opciones)

            ruta, dist_m = dijkstra(
                self.engine.graph,
                origen_ref['node'], destino_ref['node'],
                weight='length'
            )

            if not ruta:
                contador += 1
                continue

            dist_km = round(dist_m / 1000, 3)
            vehiculo.traveling = vehiculo.viajar(dist_km) # ejecuta el viaje

            # evaluacion corregida de la necesidad de carga
            if vehiculo.necesita_carga or vehiculo.bateria_critica:
                est, ruta_est, dist_est = encontrar_mas_cercana(
                    self.engine.graph, destino_ref['node'], electrolineras
                )
                if est:
                    dist_est_km = round(dist_est / 1000, 3)
                    self.logs.append({
                        "timestamp":                    datetime.now().isoformat(),
                        "vehiculo":                     vehiculo.nombre,
                        "tipo_vehiculo":                vehiculo.tipo,
                        "origen":                       origen_ref['nombre'],
                        "destino":                      destino_ref['nombre'],
                        "electrolinera":                est['nombre'],
                        "bateria_al_llegar":            vehiculo.porcentaje_bateria,
                        "distancia_recorrido_km":       dist_km,
                        "distancia_a_electrolinera_km": dist_est_km,
                        "recorrido_num":                contador + 1,
                    })
                    vehiculo.recargar(90)

            contador += 1

        print(f"simulacion terminada: {len(self.logs)} eventos de recarga registrados.")
        return self.logs