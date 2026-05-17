import folium
import os
import webbrowser
from collections import Counter

MAPA_PATH = "data/mapa_electrolineras.html"

def generar_mapa_completo(electrolineras, puntos_referencia, logs=None, engine=None):
    mapa = folium.Map(location=[7.08, -73.11], zoom_start=12, tiles="CartoDB positron")

    # Electrolineras
    g_est = folium.FeatureGroup(name="electrolineras")
    for est in electrolineras:
        folium.Marker(
            location=[est['lat'], est['lon']],
            popup=folium.Popup(f"<b>{est['nombre']}</b>", max_width=200),
            icon=folium.Icon(color='green', icon='bolt', prefix='fa'),
            tooltip=f"{est['nombre']}"
        ).add_to(g_est)
    g_est.add_to(mapa)

    #puntos de referencia
    g_ref = folium.FeatureGroup(name="puntos de referencia")
    for p in puntos_referencia:
        folium.Marker(
            location=[p['lat'], p['lon']],
            popup=folium.Popup(f"<b>{p['nombre']}</b>", max_width=200),
            icon=folium.Icon(color='blue', icon='graduation-cap', prefix='fa'),
            tooltip=f"{p['nombre']}"
        ).add_to(g_ref)
    g_ref.add_to(mapa)

    #circulos de uso segun los logs
    if logs:
        conteo = Counter(log['electrolinera'] for log in logs)
        g_heat = folium.FeatureGroup(name="intensidad de uso")
        for est in electrolineras:
            cnt = conteo.get(est['nombre'], 0)
            if cnt > 0:
                folium.Circle(
                    location=[est['lat'], est['lon']],
                    radius=cnt * 80,
                    color='orange', fill=True, fill_opacity=0.4,
                    tooltip=f"{est['nombre']}: {cnt} recargas"
                ).add_to(g_heat)
        g_heat.add_to(mapa)

    folium.LayerControl().add_to(mapa)
    os.makedirs("data", exist_ok=True)
    mapa.save(MAPA_PATH)
    print(f"mapa guardado: {MAPA_PATH}")
    webbrowser.open(f"file://{os.path.abspath(MAPA_PATH)}")