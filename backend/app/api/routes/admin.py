from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.option import Option
from app.models.question import Question
from app.schemas.question import (
    OptionCreate,
    OptionDetail,
    OptionEffectAssign,
    OptionEffectRead,
    OptionNextQuestionAssign,
    QuestionCreate,
    QuestionDetail,
    QuestionListItem,
)
from app.services.admin_service import (
    assign_next_question,
    assign_option_effect,
    create_option,
    create_question,
    get_question_or_404,
    list_questions,
)
from app.services.session_service import serialize_question

router = APIRouter()


@router.post("/questions", response_model=QuestionListItem, status_code=status.HTTP_201_CREATED)
def create_question_endpoint(payload: QuestionCreate, db: Session = Depends(get_db)) -> Question:
    return create_question(
        db,
        text=payload.text,
        is_start=payload.is_start,
        is_terminal=payload.is_terminal,
    )


@router.get("/questions", response_model=list[QuestionListItem])
def list_questions_endpoint(db: Session = Depends(get_db)) -> list[Question]:
    return list_questions(db)


@router.get("/questions/{question_id}", response_model=QuestionDetail)
def get_question_endpoint(question_id: int, db: Session = Depends(get_db)) -> QuestionDetail:
    question = get_question_or_404(db, question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")
    return serialize_question(question)


@router.post(
    "/questions/{question_id}/options",
    response_model=OptionDetail,
    status_code=status.HTTP_201_CREATED,
)
def create_option_endpoint(
    question_id: int, payload: OptionCreate, db: Session = Depends(get_db)
) -> OptionDetail:
    question = db.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")
    option = create_option(db, question=question, text=payload.text)
    return OptionDetail(
        id=option.id,
        text=option.text,
        created_at=option.created_at,
        effects=[],
        next_question_id=None,
    )


@router.post(
    "/options/{option_id}/effects",
    response_model=OptionEffectRead,
    status_code=status.HTTP_201_CREATED,
)
def assign_effect_endpoint(
    option_id: int, payload: OptionEffectAssign, db: Session = Depends(get_db)
) -> OptionEffectRead:
    option = db.get(Option, option_id)
    if not option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opción no encontrada")
    effect = assign_option_effect(
        db, option=option, dimension=payload.dimension.value, value=payload.value
    )
    return effect


@router.post(
    "/options/{option_id}/next-question",
    status_code=status.HTTP_201_CREATED,
)
def assign_next_question_endpoint(
    option_id: int, payload: OptionNextQuestionAssign, db: Session = Depends(get_db)
) -> dict[str, int]:
    option = db.get(Option, option_id)
    if not option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opción no encontrada")

    next_question = db.get(Question, payload.next_question_id)
    if not next_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pregunta siguiente no encontrada",
        )

    link = assign_next_question(db, option=option, next_question=next_question)
    return {"id": link.id, "option_id": link.option_id, "next_question_id": link.next_question_id}
