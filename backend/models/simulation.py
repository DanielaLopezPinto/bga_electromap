# backend/models/simulation.py
from math import dist
import networkx as nx
import json
import os
from datetime import datetime
import random

class SimulationManager:
    def __init__(self, data_file="backend/data/simulation_logs.json"):
        self.data_file = data_file
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

    def save_recharge_event(self, vehicle_type: str, station_name: str, battery_level: float):
        if not (10 <= battery_level <= 20):
            return {"error": "el nivel de batería debe estar entre 10% y 20% para requerir carga"}

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
        
        bateria = vehiculo["bateria_max"]
        
        manager = SimulationManager()
        
        print("\n==============================")
        print(f"Vehículo: {vehiculo['nombre']}")
        print(f"Batería actual: {bateria:.2f} kWh")
        
        origen = random.choice(self.puntos)
        for i in range(n):
            
            destino = random.choice(self.puntos)

            max_intentos = 10
            intentos = 0

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
            
            
            distancia = self.engine.get_route_distance(ruta)
            consumo = self.compute_consumption(distancia, vehiculo)
            
            bateria -= consumo

            print(
                f"[Viaje #{i+1}] "
                f"{origen['nombre']} → {destino['nombre']} | "
                f"Distancia: {distancia:.0f} m | "
                f"Consumo: {consumo:.2f} kWh | "
                f"Batería: {bateria:.2f} kWh"
            )
            
            
            umbral = 0.2 * vehiculo["bateria_max"]
            
            if bateria <= umbral:
                current_node = ruta[-1]
                print(f"\nUbicación actual: {destino['nombre']}")
                print(f"Nodo actual: {current_node}")
                print("\nBatería baja")
                print(f"Batería restante: {bateria:.2f} kWh")

                estacion, _, _ = self.engine.nearest_charging_station(
                    current_node,
                    self.electrolineras
                )
                
                if estacion is None:
                    print("---No se encontró estación cercana---")
                    continue

                estacion_node = estacion["node"]

                consumo_kwh_km = vehiculo["Wh_por_km"] / 1000
                self.engine.energy_weight(consumo_kwh_km)

                # Ruta más corta
                ruta_corta = self.engine.get_shortest_path(
                    current_node,
                    estacion_node
                )

                # Ruta más eficiente
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
                    "estacion": estacion["nombre"],
                    "bateria_restante": bateria,
                    "distancia_a_estacion": round(dist_final, 2),
                    "mejor_ruta": mejor_opcion
                })

                bateria = vehiculo["bateria_max"]
                
            else:
                self.registros.append({
                    "vehiculo": vehiculo["nombre"],
                    "evento": "viaje",
                    "origen": origen["nombre"],
                    "destino": destino["nombre"],
                    "bateria_restante": bateria,
                    "distancia": distancia
                })
            
            origen = destino
    
    def guardar_dataset(self, archivo="backend/data/simulation_dataset.json"):
        
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        with open(archivo, 'w', encoding="utf-8") as f:
            json.dump(self.registros, f, indent=4, ensure_ascii=False)
            
            