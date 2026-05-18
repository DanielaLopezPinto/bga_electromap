# backend/models/simulation.py
from math import dist
import networkx as nx
import json
import os
from datetime import datetime
import random

class SimulationManager:
# Archivo donde se guardarán los logs de recarga
    def __init__(self, data_file="data/simulation_logs.json"):
        self.data_file = data_file
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

# Guarda un evento de recarga en un archivo JSON
    def save_recharge_event(self, vehicle_type: str, station_name: str, battery_level: float):
        if not (10 <= battery_level <= 20):
            return {"Error": "El nivel de batería debe estar entre 10% y 20% para requerir carga"}

        new_event = {
            "timestamp": datetime.now().isoformat(),
            "vehicle_type": vehicle_type,
            "station": station_name,
            "battery_at_arrival": battery_level
        }

        try:
            data = []
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
            
            data.append(new_event)

            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            return {"status": "success", "message": "Recarga registrada correctamente."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
class Simulation:
    
    def __init__(self, engine, electrolineras, puntos):
        self.engine = engine
        self.electrolineras = electrolineras
        self.puntos = puntos
        self.registros = []
        
    def compute_consumption(self, distancia_m, vehiculo):
        """
        Calcula el consumo energético del vehículo en kWh
        basado en la distancia recorrida.
        """
        return (distancia_m / 1000) * (vehiculo["Wh_por_km"]/ 1000)
    
    
    
    def simulate(self, vehiculo, n=5):
        """Simula n viajes aleatorios para un vehículo dado"""
        bateria = vehiculo["bateria_max"]
        manager = SimulationManager()
        print("\n==============================")
        print(f"Vehículo: {vehiculo['nombre']}")
        print(f"Batería actual: {bateria:.2f} kWh")
        
        origen = random.choice(self.puntos)
        for i in range(n):
            
            destino = random.choice(self.puntos)
            # evita bucles infinitos
            max_intentos = 10
            intentos = 0
            # evita que el carro salga y llegue al mismo lugar.
            while destino["node"] == origen["node"] and intentos < max_intentos:
                destino = random.choice(self.puntos)
                intentos += 1

            if intentos == max_intentos:
                print("---No se pudo encontrar destino válido---")
                continue
            
            try:
                ruta = self.engine.get_route_by_coords(
                    origen["lat"], origen["lon"],
                    destino["lat"], destino["lon"]
                )
            except nx.NetworkXNoPath:
                print(f"No hay ruta entre {origen['nombre']} y {destino['nombre']}, se omite")
                continue
            
            distancia_total = 0
            consumo_total = 0
            viaje_interrumpido = False
            for j in range(len(ruta) - 1):
                
                u = ruta[j]
                v = ruta[j + 1]

                edge_data = self.engine.graph.get_edge_data(u, v)[0]

                distancia_tramo = edge_data["length"]

                consumo_tramo = self.compute_consumption(
                    distancia_tramo,
                    vehiculo
                )

                bateria -= consumo_tramo

                distancia_total += distancia_tramo
                consumo_total += consumo_tramo

                umbral = 0.2 * vehiculo["bateria_max"]

                # revisa la batería durante el trayecto
                if bateria <= umbral:

                    print("\n--- Batería baja durante el trayecto ---")

                    current_node = v
                    
                    node_data = self.engine.graph.nodes[current_node]

                    lat_actual = node_data["y"]
                    lon_actual = node_data["x"]

                    print(f"Ubicación parcial del recorrido")
                    print(f"Nodo actual: {current_node}")
                    print(f"Coordenadas actuales: ({lat_actual}, {lon_actual})")
                    print(f"Batería restante: {bateria:.2f} kWh")

                    print(
                        f"Mapa: https://www.google.com/maps?q={lat_actual},{lon_actual}"
                    )

                    estacion, _, _ = self.engine.nearest_charging_station(
                        current_node,
                        self.electrolineras
                    )

                    if estacion is None:
                        print("--- No se encontró estación cercana ---")
                        break

                    estacion_node = estacion["node"]

                    consumo_kwh_km = vehiculo["Wh_por_km"] / 1000
                    self.engine.energy_weight(consumo_kwh_km)

                    ruta_corta = self.engine.get_shortest_path(
                        current_node,
                        estacion_node
                    )

                    ruta_ef = self.engine.get_most_efficient_path(
                        current_node,
                        estacion_node
                    )

                    dist_corta = self.engine.get_route_distance(ruta_corta)
                    dist_ef = self.engine.get_route_distance(ruta_ef)

                    consumo_corto = self.engine.get_route_consumption(ruta_corta)
                    consumo_ef = self.engine.get_route_consumption(ruta_ef)

                    print("\nComparación hacia electrolinera")
                    print(f"Electrolinera: {estacion['nombre']}")

                    print("\nRuta más corta:")
                    print(
                        f"Distancia: {dist_corta:.2f} m | "
                        f"Consumo: {consumo_corto:.4f} kWh"
                        )

                    print("\nRuta más eficiente:")
                    print(
                        f"Distancia: {dist_ef:.2f} m | "
                        f"Consumo: {consumo_ef:.4f} kWh"
                    )

                    if consumo_ef < consumo_corto:
                        mejor_opcion = "Ruta eficiente"
                        ruta_final = ruta_ef
                        dist_final = dist_ef
                    else:
                        mejor_opcion = "Ruta corta"
                        ruta_final = ruta_corta
                        dist_final = dist_corta

                    print(f"\nMejor opción: {mejor_opcion}")
                
                    battery_percent = (
                        bateria / vehiculo["bateria_max"]
                    ) * 100

                    # Guarda el evento de recarga en el dataset JSON
                    manager.save_recharge_event(
                        vehiculo["nombre"],
                        estacion["nombre"],
                        battery_percent
                    )

                    # Guarda también el evento en memoria
                    self.registros.append({
                        "vehiculo": vehiculo["nombre"],
                        "evento": "recarga",
                        "origen": origen["nombre"],
                        "destino": destino["nombre"],
                        "estacion": estacion["nombre"],
                        "bateria_restante": round(battery_percent, 2),
                        "distancia_recorrida": round(distancia_total, 2),
                        "consumo_total": round(consumo_total, 2),
                        "distancia_a_estacion": round(dist_final, 2),
                        "mejor_ruta": mejor_opcion,
                        "mapa": f"https://www.google.com/maps?q={lat_actual},{lon_actual}"
                    })

                    bateria = vehiculo["bateria_max"]
                    origen = estacion
                    viaje_interrumpido = True
                    break
                
            if not viaje_interrumpido:
                
                print(
                f"[Viaje #{i+1}] "
                f"{origen['nombre']} → {destino['nombre']} | "
                f"Distancia: {distancia_total:.0f} m | "
                f"Consumo: {consumo_total:.2f} kWh | "
                f"Batería: {bateria:.2f} kWh"
                )
                
                self.registros.append({
                    "vehiculo": vehiculo["nombre"],
                    "evento": "viaje",
                    "origen": origen["nombre"],
                    "destino": destino["nombre"],
                    "bateria_restante": bateria,
                    "distancia": round(distancia_total, 2),
                    "consumo": round(consumo_total, 2)
                })
                origen = destino
    
    
    def guardar_dataset(self, archivo="data/simulation_dataset.json"):
        
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        with open(archivo, 'w', encoding="utf-8") as f:
            json.dump(self.registros, f, indent=4, ensure_ascii=False)
            
            