from collections.abc import Mapping

from app.core.config import settings
from app.core.enums import Dimension, FinalResult

DIMENSION_WEIGHTS: dict[Dimension, float] = {
    Dimension.comunicacion: 0.20,
    Dimension.respeto: 0.25,
    Dimension.coherencia: 0.20,
    Dimension.responsabilidad_afectiva: 0.25,
    Dimension.interes_real: 0.10,
}


def validate_weights() -> None:
    total = round(sum(DIMENSION_WEIGHTS.values()), 10)
    if total != 1.0:
        raise ValueError(f"La suma de pesos debe ser 1.0 y actualmente es {total}")


validate_weights()


def empty_dimension_scores() -> dict[Dimension, int]:
    return {dimension: 0 for dimension in Dimension}


def normalize_dimension(raw_value: int) -> float:
    min_score = settings.dimension_min_score
    max_score = settings.dimension_max_score
    if min_score >= max_score:
        raise ValueError("dimension_min_score debe ser menor que dimension_max_score")

    bounded = max(min(raw_value, max_score), min_score)
    return round(((bounded - min_score) / (max_score - min_score)) * 100, 2)


def normalize_dimensions(raw_scores: Mapping[Dimension, int]) -> dict[Dimension, float]:
    return {
        dimension: normalize_dimension(raw_scores.get(dimension, 0))
        for dimension in Dimension
    }


def calculate_final_score(normalized_scores: Mapping[Dimension, float]) -> float:
    return round(
        sum(normalized_scores.get(dimension, 0.0) * weight for dimension, weight in DIMENSION_WEIGHTS.items()),
        2,
    )


def classify_score(score: float) -> FinalResult:
    if score >= 70:
        return FinalResult.green_flag
    if score >= 40:
        return FinalResult.zona_gris
    return FinalResult.red_flag
