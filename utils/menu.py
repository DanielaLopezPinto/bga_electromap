def mostrar_encabezado():
    print("\n" + "="*60)
    print("   BGA ELECTROMAP")
    print("   sistema de Electrolineras — Área Metropolitana BGA")
    print("="*60)

def mostrar_menu_principal():
    print("\n  MENÚ PRINCIPAL")
    print("  1.  Ver electrolineras y puntos")
    print("  2.  Cargar mapa vial (OSMnx)")
    print("  3.  Calcular ruta más corta")
    print("  4.  Ejecutar simulación")
    print("  5.  Ver estadísticas")
    print("  6.  Entrenar modelo ML")
    print("  7.  Predicción con modelo ML")
    print("  8.  Mapa interactivo (Folium)")
    print("  9.  Gráficas (Plotly)")
    print("  10. Exportar datos")
    print("  0.  Salir")
    print("\n  Opción: ", end="")

def separador():
    print("\n" + "-"*60)

def titulo_seccion(titulo):
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")