## bga_electromap

### descripción

este proyecto propone una solución al problema de distribución e infraestructura de
electrolineras en el área metropolitana de Bucaramanga. El sistema simula recorridos
aleatorios de vehículos eléctricos sobre la red vial real obtenida desde OpenStreetMap.
Cuando la batería de un vehículo cae al rango del 10% al 20%, el algoritmo de Dijkstra
calcula la ruta más corta hacia la electrolinera más cercana y registra el evento.

los datos generados por la simulación alimentan un modelo supervisado (Random Forest)
que aprende a predecir la electrolinera óptima sin necesidad de ejecutar el algoritmo
en cada consulta. Además, el sistema produce visualizaciones interactivas y
exporta los resultados en múltiples formatos para análisis posteriores.


### arquitectura

```
bga_electromap/
├── main.py                     # punto de entrada — menú CLI
├── data/
│   ├── locations.py            # coordenadas de electrolineras y puntos de referencia
│   ├── vehicles.py             # catálogo de vehículos (alta y baja gama)
│   └── simulation_logs/        # archivos generados: .json .csv .xlsx .txt
├── graph/
│   ├── graph_engine.py         # carga OSMnx, pesos energéticos, asignación de nodos
│   ├── routing.py              # Dijkstra y Floyd-Warshall (NetworkX)
│   └── nearest_station.py      # búsqueda de electrolinera más cercana
├── simulation/
│   ├── vehicle_model.py        # clase Vehiculo: batería, consumo, recarga
│   ├── simulator.py            # motor de simulación con n recorridos aleatorios
│   └── stats.py                # estadísticas de los logs de recarga
├── ml/
│   ├── dataset_builder.py      # construye dataset con rutas precalculadas (Floyd-Warshall)
│   ├── trainer.py              # entrena Random Forest (clasificación y regresión)
│   └── predictor.py            # predicción de electrolinera óptima
├── visualization/
│   ├── map_folium.py           # mapa interactivo con marcadores y rutas
│   ├── charts_plotly.py        # gráficas de estadísticas
│   └── graph_viz.py            # visualización del grafo con NetworkX + Matplotlib
└── utils/
    ├── validators.py           # validación de entradas (tipo, rango, caracteres)
    ├── file_io.py              # lectura/escritura en JSON, CSV, XLSX, TXT
    └── menu.py                 # funciones de presentación del menú CLI
```

### flujo del sistema

```
OSMnx (red vial) --> GraphEngine --> asigna nodos a electrolineras y puntos de referencia
                                          |
                          simulator: n recorridos aleatorios
                                          |
                    bateria en 10-20% --> Dijkstra --> electrolinera mas cercana
                                          |
                                   logs de recarga
                                    /           \
                          Floyd-Warshall       estadísticas
                                |
                          dataset supervisado
                                |
                      entrenamiento random Forest
                                |
                    prediccion de electrolinera optima
```

### instalacion

```bash
git clone https://github.com/arcibyte/bga_electromap
cd bga_electromap
pip install -r requirements.txt
python main.py
```

### dependencias principales

```
osmnx        >= 1.9.0    # extraccion de red vial (OpenStreetMap)
networkx     >= 3.3      # manipulacion de grafos, Dijkstra, Floyd-Warshall
scikit-learn >= 1.5.0    # random Forest
xgboost      >= 2.0.0    # modelo alternativo de boosting
folium       >= 0.17.0   # mapas interactivos HTML
plotly       >= 5.22.0   # graficas estadisticas
pandas       >= 2.2.0    # manejo de datasets
openpyxl     >= 3.1.0    # exportacion a Excel
joblib       >= 1.4.0    # serializacion de modelos ML
matplotlib   >= 3.9.0    # visualizacion del grafo
```

### Uso

al ejecutar `python main.py` se presenta el menu principal. El orden recomendado es:

1. **opcion 2** — cargar mapa vial desde OSMnx (necesario para las demas opciones)
2. **opcion 4** — ejecutar simulacion de n recorridos
3. **opcion 5** — ver estadisticas de recargas
4. **opcion 6** — construir dataset y entrenar modelo ML
5. **opcion 7** — predecir electrolinera optima con el modelo entrenado
6. **opcion 8** — generar mapa interactivo Folium
7. **opcion 9** — generar graficas Plotly
8. **opcion 10** — exportar datos en JSON, CSV, XLSX y TXT

### archivos generados

todos los archivos se guardan en `data/`:

| archivo | descripcion |
|---------|-------------|
| `graph_cache.graphml` | grafo de la red vial en cache (evita redescargar) |
| `training_dataset.csv` | dataset de rutas para entrenamiento ML |
| `modelo_clasificacion.pkl` | modelo Random Forest serializado |
| `modelo_regresion.pkl` | modelo de regresion serializado |
| `simulation_logs/logs_*.json` | logs de recargas en JSON |
| `simulation_logs/logs_*.csv` | logs de recargas en CSV |
| `simulation_logs/logs_*.xlsx` | logs de recargas en Excel |
| `simulation_logs/logs_*.txt` | resumen de recargas en texto plano |
| `mapa_electrolineras.html` | mapa interactivo Folium |
| `grafica_recargas.html` | grafica de barras por electrolinera |
| `grafica_bateria.html` | histograma de niveles de bateria |
| `grafica_vehiculos.html` | grafica de torta por tipo de vehiculo |
| `grafo_red_vial.png` | visualizacion del grafo con nodos marcados |

### estructura de un log de recarga

```json
{
    "timestamp": "2026-05-17T10:32:45",
    "vehiculo": "BYD Han EV",
    "tipo_vehiculo": "alta_gama",
    "origen": "UIS Campus Central",
    "destino": "UNAB",
    "electrolinera": "CC Cacique",
    "bateria_al_llegar": 14.5,
    "distancia_recorrido_km": 3.21,
    "distancia_a_electrolinera_km": 0.87,
    "recorrido_num": 3
}
```
### algoritmos implementados

**Dijkstra** usado durante la simulacion en tiempo real para encontrar la ruta mas corta
desde la posicion actual del vehiculo hasta cada electrolinera. Complejidad: O((V + E) log V)

**Floyd-Warshall** usado una sola vez para precalcular rutas entre todos los pares de nodos
clave (electrolineras + puntos de referencia). Sus resultados construyen el dataset de
entrenamiento del modelo ML. Complejidad: O(V^3)

**random Forest** modelo supervisado que aprende de las rutas precalculadas. Predice
(a) cual electrolinera es la optima (clasificacion) y (b) la distancia estimada hasta ella
(regresion), sin necesidad de ejecutar Dijkstra en cada consulta.


### vehiculos

| vehiculo | tipo | bateria (kWh) | autonomia (km) |
|----------|------|---------------|----------------|
| BYD Han EV | alta gama | 76.9 | 610 |
| Tesla Model 3 Long Range | alta gama | 82.0 | 602 |
| Renault Kwid E-Tech | baja gama | 26.8 | 300 |
| Nissan Leaf | baja gama | 40.0 | 270 |


### referencias

- Rosen, K. *Discrete Mathematics and its Applications*. McGraw-Hill, 2011.
- OSMnx documentation: https://osmnx.readthedocs.io
- NetworkX documentation: https://networkx.org
- scikit-learn documentation: https://scikit-learn.org
- EV Database: https://ev-database.org/cheatsheet/range-electric-car
