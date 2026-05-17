import json
import csv
import os
from datetime import datetime

def guardar_json(datos, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    print(f"JSON guardado: {ruta}")

def cargar_json(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_csv(datos, ruta, campos):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos)
    print(f"CSV guardado: {ruta}")

def cargar_csv(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def guardar_xlsx(datos, ruta, hoja="Datos"):
    import openpyxl
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = hoja
    if datos:
        ws.append(list(datos[0].keys()))
        for fila in datos:
            ws.append(list(fila.values()))
    wb.save(ruta)
    print(f"Excel guardado: {ruta}")

def guardar_txt(texto, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(texto)
    print(f"TXT guardado: {ruta}")

def exportar_logs_todos_formatos(logs, carpeta="data/simulation_logs"):
    if not logs:
        print("!no hay logs para exportar.")
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{carpeta}/logs_{ts}"
    campos = list(logs[0].keys())

    guardar_json(logs, f"{base}.json")
    guardar_csv(logs, f"{base}.csv", campos)
    guardar_xlsx(logs, f"{base}.xlsx", "recargas")

    resumen = f"LOG DE SIMULACIÓN\nfecha: {datetime.now()}\ntotal recargas: {len(logs)}\n\n"
    for log in logs:
        resumen += (f"[{log.get('timestamp','')}] "
                    f"{log.get('vehiculo','')} → "
                    f"{log.get('electrolinera','')} | "
                    f"batería: {log.get('bateria_al_llegar','')}%\n")
    guardar_txt(resumen, f"{base}.txt")
    print(f"exportación completa en: {carpeta}")