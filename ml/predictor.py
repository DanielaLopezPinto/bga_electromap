import numpy as np
from ml.trainer import cargar_modelos, FEATURES

def predecir_electrolinera(lat, lon, bateria_pct, electrolineras):
    clf, reg, le = cargar_modelos()
    if clf is None:
        return {"error": "Modelo no entrenado. Ejecute la opción 6 primero."}

    #feature: distancia euclidiana al centroide de electrolineras
    c_lat = sum(e['lat'] for e in electrolineras) / len(electrolineras)
    c_lon = sum(e['lon'] for e in electrolineras) / len(electrolineras)
    dist_eucl = np.sqrt((lat - c_lat) ** 2 + (lon - c_lon) ** 2)

    X = np.array([[lat, lon, bateria_pct, dist_eucl]])

    clase_pred   = clf.predict(X)[0]
    proba        = clf.predict_proba(X)[0]
    dist_pred    = reg.predict(X)[0]
    est_id       = int(le.inverse_transform([clase_pred])[0])
    est_info     = next((e for e in electrolineras if e['id'] == est_id), None)

    return {
        "electrolinera_id":      est_id,
        "electrolinera_nombre":  est_info['nombre'] if est_info else "Desconocida",
        "distancia_estimada_m":  round(dist_pred, 2),
        "distancia_estimada_km": round(dist_pred / 1000, 3),
        "confianza_pct":         round(max(proba) * 100, 2),
    }

def comparar_con_dijkstra(prediccion, distancia_dijkstra_m):
    error_m   = abs(prediccion['distancia_estimada_m'] - distancia_dijkstra_m)
    error_pct = round(error_m / max(distancia_dijkstra_m, 1) * 100, 2)
    return {
        "distancia_ml_m":       prediccion['distancia_estimada_m'],
        "distancia_dijkstra_m": distancia_dijkstra_m,
        "error_absoluto_m":     round(error_m, 2),
        "error_porcentual_pct": error_pct,
    }