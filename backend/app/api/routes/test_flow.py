from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.question import QuestionDetail
from app.schemas.session import AnswerRequest, NextQuestionPayload, SessionCreated, SessionResult
from app.services.session_service import (
    answer_question,
    calculate_session_result,
    get_session_or_404,
    get_start_question,
    serialize_question,
    start_session,
)

router = APIRouter()


@router.post("/sessions", response_model=SessionCreated)
def start_session_endpoint(db: Session = Depends(get_db)):
    return start_session(db)


@router.get("/sessions/{session_id}/start", response_model=QuestionDetail)
def get_start_question_endpoint(session_id: int, db: Session = Depends(get_db)) -> QuestionDetail:
    get_session_or_404(db, session_id)
    return serialize_question(get_start_question(db))


@router.post("/sessions/{session_id}/answers", response_model=NextQuestionPayload)
def answer_question_endpoint(
    session_id: int, payload: AnswerRequest, db: Session = Depends(get_db)
) -> NextQuestionPayload:
    return answer_question(
        db,
        session_id=session_id,
        question_id=payload.question_id,
        option_id=payload.option_id,
    )


@router.get("/sessions/{session_id}/result", response_model=SessionResult)
def session_result_endpoint(session_id: int, db: Session = Depends(get_db)) -> SessionResult:
    session = get_session_or_404(db, session_id)
    if not session.finished_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sesión aún no ha finalizado",
        )
    return calculate_session_result(db, session_id)
