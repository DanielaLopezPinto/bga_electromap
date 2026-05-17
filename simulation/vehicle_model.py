class Vehiculo:
    def __init__(self, datos):
        self.id               = datos['id']
        self.nombre           = datos['nombre']
        self.tipo             = datos['tipo']
        self.capacidad_kwh    = datos['capacidad_bateria_kwh']
        self.autonomia_km     = datos['autonomia_km']
        self.consumo_kwh_km   = datos['consumo_kwh_por_km']
        self.bateria_actual   = self.capacidad_kwh   # Empieza al 100%
        self.total_recargas   = 0
        self.km_recorridos    = 0.0

    @property
    def porcentaje_bateria(self):
        return round((self.bateria_actual / self.capacidad_kwh) * 100, 2)

    @property
    def necesita_carga(self):
        # alerta activa para cualquier nivel inferior o igual al 20%
        return self.porcentaje_bateria <= 20.0

    @property
    def bateria_critica(self):
        return self.porcentaje_bateria < 10.0

    def viajar(self, distancia_km):
        """Consume batería según la distancia. Retorna True si llegó bien."""
        # MODIFICACIÓN DE DEPURACIÓN: Se multiplica el consumo por 25 
        # para simular un desgaste drástico en distancias cortas urbanas.
        energia = distancia_km * self.consumo_kwh_km * 25
        
        if energia > self.bateria_actual:
            self.bateria_actual = 0.0
            self.km_recorridos += distancia_km
            return False
            
        self.bateria_actual -= energia
        self.km_recorridos  += distancia_km
        return True

    def recargar(self, porcentaje=90):
        self.bateria_actual = (porcentaje / 100) * self.capacidad_kwh
        self.total_recargas += 1

    def __str__(self):
        return (f"{self.nombre} [{self.tipo}] | "
                f"batería: {self.porcentaje_bateria}% | "
                f"recargas: {self.total_recargas} | "
                f"KM: {round(self.km_recorridos, 2)}")