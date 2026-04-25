from enum import Enum


class Dimension(str, Enum):
    comunicacion = "comunicacion"
    respeto = "respeto"
    coherencia = "coherencia"
    responsabilidad_afectiva = "responsabilidad_afectiva"
    interes_real = "interes_real"
    honestidad = "honestidad"
    confianza = "confianza"
    limites_personales = "limites_personales"
    manipulacion = "manipulacion"
    celos_control = "celos_control"
    disponibilidad_emocional = "disponibilidad_emocional"
    compromiso = "compromiso"
    empatia = "empatia"
    resolucion_conflictos = "resolucion_conflictos"
    reciprocidad = "reciprocidad"


class FinalResult(str, Enum):
    green_flag = "Green Flag"
    zona_gris = "Zona Gris"
    red_flag = "Red Flag"
