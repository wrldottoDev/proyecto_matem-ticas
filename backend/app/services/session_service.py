from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import Dimension
from app.core.scoring import (
    calculate_final_score,
    classify_score,
    empty_dimension_scores,
    normalize_dimensions,
)
from app.models.option import Option
from app.models.question import Question
from app.models.session import Session as TestSession
from app.models.session import SessionAnswer
from app.schemas.question import OptionDetail, QuestionDetail
from app.schemas.session import DimensionScores, NextQuestionPayload, SessionResult


def start_session(db: Session) -> TestSession:
    session = TestSession()
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session_or_404(db: Session, session_id: int) -> TestSession:
    session = db.get(TestSession, session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sesión no encontrada")
    return session


def get_start_question(db: Session) -> Question:
    statement = (
        select(Question)
        .where(Question.is_start.is_(True))
        .options(
            joinedload(Question.options).joinedload(Option.effects),
            joinedload(Question.options).joinedload(Option.next_question_link),
        )
    )
    question = db.scalars(statement).unique().one_or_none()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe una pregunta inicial configurada",
        )
    return question


def serialize_question(question: Question) -> QuestionDetail:
    ordered_options = sorted(question.options, key=lambda option: option.id)
    return QuestionDetail(
        id=question.id,
        text=question.text,
        is_start=question.is_start,
        is_terminal=question.is_terminal,
        created_at=question.created_at,
        options=[
            OptionDetail(
                id=option.id,
                text=option.text,
                created_at=option.created_at,
                effects=option.effects,
                next_question_id=(
                    option.next_question_link.next_question_id if option.next_question_link else None
                ),
            )
            for option in ordered_options
        ],
    )


def calculate_session_result(db: Session, session_id: int) -> SessionResult:
    statement = (
        select(SessionAnswer)
        .where(SessionAnswer.session_id == session_id)
        .options(joinedload(SessionAnswer.option).joinedload(Option.effects))
    )
    answers = list(db.execute(statement).unique().scalars().all())

    raw_scores = empty_dimension_scores()
    for answer in answers:
        for effect in answer.option.effects:
            raw_scores[Dimension(effect.dimension)] += effect.value

    normalized = normalize_dimensions(raw_scores)
    final_score = calculate_final_score(normalized)
    final_result = classify_score(final_score)

    return SessionResult(
        session_id=session_id,
        final_score=final_score,
        final_result=final_result,
        raw_scores=DimensionScores(**{dimension.value: float(value) for dimension, value in raw_scores.items()}),
        normalized_scores=DimensionScores(
            **{dimension.value: value for dimension, value in normalized.items()}
        ),
    )


def finalize_session(db: Session, session: TestSession) -> SessionResult:
    result = calculate_session_result(db, session.id)
    session.finished_at = datetime.now(timezone.utc)
    session.final_score = result.final_score
    session.final_result = result.final_result.value
    db.commit()
    db.refresh(session)
    return result


def answer_question(
    db: Session, *, session_id: int, question_id: int, option_id: int
) -> NextQuestionPayload:
    session = get_session_or_404(db, session_id)
    if session.finished_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sesión ya está finalizada",
        )

    question = db.scalar(select(Question).where(Question.id == question_id))
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")

    option = db.scalar(
        select(Option)
        .where(Option.id == option_id)
        .options(joinedload(Option.effects), joinedload(Option.next_question_link))
    )
    if not option:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opción no encontrada")
    if option.question_id != question.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La opción no pertenece a la pregunta indicada",
        )

    already_answered = db.scalar(
        select(SessionAnswer).where(
            SessionAnswer.session_id == session.id,
            SessionAnswer.question_id == question.id,
        )
    )
    if already_answered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pregunta ya fue respondida en esta sesión",
        )

    answer = SessionAnswer(session_id=session.id, question_id=question.id, option_id=option.id)
    db.add(answer)
    db.commit()

    should_finish = question.is_terminal or option.next_question_link is None
    if should_finish:
        result = finalize_session(db, session)
        return NextQuestionPayload(question=None, session_finished=True, result=result)

    next_question = db.scalars(
        select(Question)
        .where(Question.id == option.next_question_link.next_question_id)
        .options(
            joinedload(Question.options).joinedload(Option.effects),
            joinedload(Question.options).joinedload(Option.next_question_link),
        )
    ).unique().one_or_none()
    if not next_question:
        result = finalize_session(db, session)
        return NextQuestionPayload(question=None, session_finished=True, result=result)

    return NextQuestionPayload(
        question=serialize_question(next_question),
        session_finished=False,
        result=None,
    )
