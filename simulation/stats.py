from collections import Counter

def generar_estadisticas(logs):
    if not logs:
        return {"error": "sin datos de simulación."}

    conteo_est    = Counter(log['electrolinera']  for log in logs)
    conteo_tipo   = Counter(log['tipo_vehiculo']  for log in logs)
    conteo_vehic  = Counter(log['vehiculo']       for log in logs)
    baterias      = [log['bateria_al_llegar']            for log in logs]
    dist_est      = [log.get('distancia_a_electrolinera_km', 0) for log in logs]
    dist_rec      = [log.get('distancia_recorrido_km', 0)       for log in logs]

    return {
        "total_recargas":                    len(logs),
        "recargas_por_electrolinera":        dict(conteo_est),
        "recargas_por_tipo_vehiculo":        dict(conteo_tipo),
        "recargas_por_vehiculo":             dict(conteo_vehic),
        "electrolinera_mas_usada":           conteo_est.most_common(1)[0] if conteo_est else None,
        "bateria_promedio_al_recargar":      round(sum(baterias) / len(baterias), 2),
        "distancia_promedio_a_estacion_km":  round(sum(dist_est) / len(dist_est), 3),
        "distancia_promedio_recorrido_km":   round(sum(dist_rec) / len(dist_rec), 3),
    }

def imprimir_estadisticas(stats):
    if "error" in stats:
        print(f" [!] {stats['error']}")
        return

    print(f"\n total recargas:              {stats['total_recargas']}")
    print(f" batería prom. al recargar:   {stats['bateria_promedio_al_recargar']}%")
    print(f" distancia prom. a estación:  {stats['distancia_promedio_a_estacion_km']} km")
    print(f" distancia prom. recorrido:   {stats['distancia_promedio_recorrido_km']} km")

    print("\n  recargas por electrolinera:")
    for nombre, cnt in sorted(stats['recargas_por_electrolinera'].items(), key=lambda x: -x[1]):
        barra = "█" * cnt
        print(f"    {nombre:<32} {barra} ({cnt})")

    print("\n recargas por tipo de vehículo:")
    for tipo, cnt in stats['recargas_por_tipo_vehiculo'].items():
        print(f"    {tipo:<20}: {cnt}")

    if stats['electrolinera_mas_usada']:
        nombre, cnt = stats['electrolinera_mas_usada']
        print(f"\n electrolinera más usada: {nombre} ({cnt} recargas)")