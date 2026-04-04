from enum import Enum


class Dimension(str, Enum):
    comunicacion = "comunicacion"
    respeto = "respeto"
    coherencia = "coherencia"
    responsabilidad_afectiva = "responsabilidad_afectiva"
    interes_real = "interes_real"


class FinalResult(str, Enum):
    green_flag = "Green Flag"
    zona_gris = "Zona Gris"
    red_flag = "Red Flag"
