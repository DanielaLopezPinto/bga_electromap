import os
import webbrowser
import plotly.graph_objects as go
import plotly.express as px

def _abrir(ruta):
    webbrowser.open(f"file://{os.path.abspath(ruta)}")

def grafica_recargas_por_electrolinera(stats):
    data = stats.get('recargas_por_electrolinera', {})
    if not data:
        print("!sin datos.")
        return
    fig = go.Figure(go.Bar(
        x=list(data.keys()), y=list(data.values()),
        marker_color='#27ae60', text=list(data.values()), textposition='outside'
    ))
    fig.update_layout(title="recargas por electrolinera",
                      xaxis_title="electrolinera", yaxis_title="recargas",
                      template="plotly_white")
    ruta = "data/grafica_recargas.html"
    fig.write_html(ruta); _abrir(ruta)
    print(f"gráfica guardada: {ruta}")

def grafica_distribucion_bateria(logs):
    if not logs:
        print("!sin datos.")
        return
    baterias = [log['bateria_al_llegar'] for log in logs]
    fig = px.histogram(x=baterias, nbins=10,
                       title="nivel de batería al recargar",
                       labels={'x': 'batería (%)', 'y': 'frecuencia'},
                       color_discrete_sequence=['#2980b9'])
    fig.update_layout(template="plotly_white")
    ruta = "data/grafica_bateria.html"
    fig.write_html(ruta); _abrir(ruta)
    print(f"grafica guardada: {ruta}")

def grafica_pie_vehiculos(stats):
    data = stats.get('recargas_por_tipo_vehiculo', {})
    if not data:
        print("!sin datos")
        return
    fig = px.pie(names=list(data.keys()), values=list(data.values()),
                 title="recargas por tipo de vehículo",
                 color_discrete_sequence=['#27ae60', '#e74c3c'])
    ruta = "data/grafica_vehiculos.html"
    fig.write_html(ruta); _abrir(ruta)
    print(f"gráfica guardada: {ruta}")