# vehiculos seleccionados de ev-database.org
# alta gama: BYD Han EV, Tesla Model 3 Long Range
# baja gama:  Renault Kwid E-Tech, Nissan Leaf

VEHICULOS = {
    "alta_gama": [
        {
            "id": "V001",
            "nombre": "BYD Han EV",
            "tipo": "alta_gama",
            "capacidad_bateria_kwh": 76.9,
            "autonomia_km": 610,
            "consumo_kwh_por_km": round(76.9 / 610, 4),
            "velocidad_max_kmh": 180,
        },
        {
            "id": "V002",
            "nombre": "Tesla Model 3 Long Range",
            "tipo": "alta_gama",
            "capacidad_bateria_kwh": 82.0,
            "autonomia_km": 602,
            "consumo_kwh_por_km": round(82.0 / 602, 4),
            "velocidad_max_kmh": 225,
        },
    ],
    "baja_gama": [
        {
            "id": "V003",
            "nombre": "Renault Kwid E-Tech",
            "tipo": "baja_gama",
            "capacidad_bateria_kwh": 26.8,
            "autonomia_km": 300,
            "consumo_kwh_por_km": round(26.8 / 300, 4),
            "velocidad_max_kmh": 130,
        },
        {
            "id": "V004",
            "nombre": "Nissan Leaf",
            "tipo": "baja_gama",
            "capacidad_bateria_kwh": 40.0,
            "autonomia_km": 270,
            "consumo_kwh_por_km": round(40.0 / 270, 4),
            "velocidad_max_kmh": 150,
        },
    ],
}

def obtener_todos():
    todos = []
    for tipo in VEHICULOS.values():
        todos.extend(tipo)
    return todos

def obtener_por_id(vid):
    for v in obtener_todos():
        if v["id"] == vid:
            return v
    return None