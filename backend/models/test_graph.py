from graph_engine import GraphEngine
from simulation import Simulation
from data import carros, electrolineras, puntos_referencia

engine = GraphEngine()
engine.load_map()
engine.assign_nodes(electrolineras)
engine.assign_nodes(puntos_referencia)

sim = Simulation(engine, electrolineras, puntos_referencia)

for carro in carros:
    print(f"\nSimulando: {carro['nombre']}")
    sim.simulate(carro, 300)
sim.guardar_dataset()