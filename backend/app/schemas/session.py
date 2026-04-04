from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import FinalResult


class SessionCreated(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    started_at: datetime


class AnswerRequest(BaseModel):
    question_id: int
    option_id: int


class NextQuestionPayload(BaseModel):
    question: "QuestionDetail | None"
    session_finished: bool
    result: "SessionResult | None" = None


class DimensionScores(BaseModel):
    comunicacion: float
    respeto: float
    coherencia: float
    responsabilidad_afectiva: float
    interes_real: float


class SessionResult(BaseModel):
    session_id: int
    final_score: float
    final_result: FinalResult
    raw_scores: DimensionScores
    normalized_scores: DimensionScores


from app.schemas.question import QuestionDetail

NextQuestionPayload.model_rebuild()
