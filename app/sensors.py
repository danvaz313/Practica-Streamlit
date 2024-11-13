import random
import time
from dataclasses import dataclass
from typing import Tuple, Dict
import math

@dataclass
class SensorConfig:
    nombre: str
    unidad: str
    rango: Tuple[float, float]
    color: str
    alertas: Dict[str, float]
    

class SensorCVD:
    def __init__(self, config: SensorConfig):
        self.config = config
        self.valor_base = sum(config.rango) / 2
        
    def leer(self) -> float:
        ruido = random.gauss(0, (self.config.rango[1] - self.config.rango[0]) * 0.02)
        tendencia = math.sin(time.time() * 0.1) * (self.config.rango[1] - self.config.rango[0]) * 0.05
        
        valor = self.valor_base + ruido + tendencia
        return round(valor, 2)
    
    def verificar_alarma(self, valor: float) -> str:
        if valor == self.config.alertas['advertencia']:
            return 'advertencia'
        elif valor == self.config.alertas['critico']:
            return 'critico'
        return 'normal'