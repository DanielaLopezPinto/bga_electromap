from fastapi import FastAPI
from typing import List, Dict
import json
import os

app = FastAPI(title="BGA Electromap API")

DATA_PATH = "backend/data/locations.json"

STATIONS = [
    {"id": 1, "name": "Homecenter", "lat": 7.1132, "lon": -73.1195},
    {"id": 2, "name": "C.C. Quinta Etapa", "lat": 7.1075, "lon": -73.1112},
    {"id": 3, "name": "C.C. Cacique", "lat": 7.1064, "lon": -73.1095},
    {"id": 4, "name": "C.C. Cañaveral", "lat": 7.0852, "lon": -73.0901},
    {"id": 5, "name": "Terpel Piedecuesta", "lat": 6.9934, "lon": -73.0612},
    {"id": 6, "name": "Éxito la Rosita", "lat": 7.1256, "lon": -73.1223},
    {"id": 7, "name": "C.C. La Florida", "lat": 7.0874, "lon": -73.0894},
    {"id": 8, "name": "Promotores del Oriente", "lat": 7.0955, "lon": -73.1550},
]

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de BGA Electromap"}

@app.get("/stations", response_model=List[Dict])
def get_stations():
    return STATIONS

@app.get("/status")
def get_status():
    return {"status": "operativo", "database": "json_file"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)