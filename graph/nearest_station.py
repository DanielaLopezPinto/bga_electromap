from graph.routing import dijkstra

def encontrar_mas_cercana(graph, nodo_actual, electrolineras):
    """
    busca la electrolinera más cercana al nodo actual con Dijkstra.
    retorna (electrolinera_dict, ruta, distancia_m).
    """
    mejor, mejor_ruta, mejor_dist = None, None, float('inf')

    for est in electrolineras:
        nodo_est = est.get('node')
        if nodo_est is None:
            continue
        ruta, distancia = dijkstra(graph, nodo_actual, nodo_est, weight='length')
        if ruta and distancia < mejor_dist:
            mejor_dist = distancia
            mejor_ruta = ruta
            mejor = est

    return mejor, mejor_ruta, mejor_dist