import pandas as pd
import numpy as np
import os
from graph.routing import floyd_warshall

DATASET_PATH = "data/training_dataset.csv"

def construir_dataset(engine, electrolineras, puntos_referencia):
    """
    usa Floyd-Warshall para precalcular rutas entre todos los nodos clave
    y construye el dataset supervisado para entrenar el modelo ML
    """
    nodos_clave = list({
        loc['node']
        for loc in list(electrolineras) + list(puntos_referencia)
        if 'node' in loc
    })

    rutas_fw = floyd_warshall(engine.graph, weight='length', nodos_subset=nodos_clave)

    filas = []
    for punto in puntos_referencia:
        if 'node' not in punto:
            continue
        nodo_origen = punto['node']

        for nivel_bat in [10, 12, 14, 16, 18, 20]:
            mejor_est  = None
            mejor_dist = float('inf')

            for est in electrolineras:
                if 'node' not in est:
                    continue
                info = rutas_fw.get(nodo_origen, {}).get(est['node'], {})
                dist = info.get('distancia', float('inf'))
                if dist < mejor_dist:
                    mejor_dist = dist
                    mejor_est  = est

            if mejor_est and mejor_dist < float('inf'):
                dist_eucl = np.sqrt(
                    (punto['lat'] - mejor_est['lat']) ** 2 +
                    (punto['lon'] - mejor_est['lon']) ** 2
                )
                filas.append({
                    'origen_lat':       punto['lat'],
                    'origen_lon':       punto['lon'],
                    'bateria_pct':      nivel_bat,
                    'dist_euclidiana':  round(dist_eucl, 6),
                    'electrolinera_id': mejor_est['id'],
                    'distancia_ruta_m': round(mejor_dist, 2),
                })

    df = pd.DataFrame(filas)
    print(f"dataset: {len(df)} muestras | {len(df.columns)} columnas")
    return df

def guardar_dataset(df, ruta=DATASET_PATH):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df.to_csv(ruta, index=False)
    print(f"dataset guardado: {ruta}")

def cargar_dataset(ruta=DATASET_PATH):
    if not os.path.exists(ruta):
        print("!no existe dataset. ejecute primero la opción 6.")
        return None
    df = pd.read_csv(ruta)
    print(f"dataset cargado: {len(df)} muestras")
    return df