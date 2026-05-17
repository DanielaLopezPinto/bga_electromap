import networkx as nx

def dijkstra(graph, origen, destino, weight='length'):
    """ruta más corta entre dos nodos con Dijkstra."""
    try:
        ruta = nx.shortest_path(graph, origen, destino, weight=weight)
        distancia = nx.shortest_path_length(graph, origen, destino, weight=weight)
        return ruta, distancia
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None, float('inf')

def floyd_warshall(graph, weight='length', nodos_subset=None):
    """
    encuentra rutas más cortas entre todos los pares de nodos (subconjunto).
    Retorna dict {origen: {destino: {ruta, distancia}}}.
    """
    print("ejecutando Floyd-Warshall (puede tardar varios minutos)...")
    subgrafo = graph.subgraph(nodos_subset) if nodos_subset else graph
    pred, dist = nx.floyd_warshall_predecessor_and_distance(subgrafo, weight=weight)

    resultados = {}
    nodos = list(subgrafo.nodes())
    for origen in nodos:
        resultados[origen] = {}
        for destino in nodos:
            if origen == destino:
                continue
            try:
                ruta = nx.reconstruct_path(origen, destino, pred)
                resultados[origen][destino] = {
                    'ruta': ruta,
                    'distancia': dist[origen][destino]
                }
            except Exception:
                resultados[origen][destino] = {'ruta': [], 'distancia': float('inf')}

    print(f"Floyd-Warshall: {len(nodos)} nodos procesados")
    return resultados