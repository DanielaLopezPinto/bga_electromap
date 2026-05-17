import json


with open("data/carros.json", encoding="utf-8") as f:
    carros = json.load(f)

with open("data/electrolineras.json", encoding="utf-8") as f:
    electrolineras = json.load(f)

with open("data/puntos_referencia.json", encoding="utf-8") as f:
    puntos_referencia = json.load(f)