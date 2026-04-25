from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.option import Option, OptionEffect, OptionNextQuestion
from app.models.question import Question


def create_question(
    db: Session,
    *,
    text: str,
    key: str | None = None,
    main_dimension: str | None = None,
    is_start: bool = False,
    is_terminal: bool = False,
) -> Question:
    if is_start:
        existing_start = db.scalar(select(Question).where(Question.is_start.is_(True)))
        if existing_start:
            existing_start.is_start = False

    question = Question(
        key=key,
        text=text,
        main_dimension=main_dimension,
        is_start=is_start,
        is_terminal=is_terminal,
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def list_questions(db: Session) -> list[Question]:
    statement = select(Question).order_by(Question.id)
    return list(db.scalars(statement).all())


def get_question_or_404(db: Session, question_id: int) -> Question:
    statement = (
        select(Question)
        .where(Question.id == question_id)
        .options(
            joinedload(Question.options)
            .joinedload(Option.effects),
            joinedload(Question.options).joinedload(Option.next_question_link),
        )
    )
    question = db.scalars(statement).unique().one_or_none()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")
    return question


def create_option(
    db: Session,
    *,
    question: Question,
    text: str,
    activates_contradiction: bool = False,
    contradiction_code: str | None = None,
    contradiction_penalty: int = 0,
) -> Option:
    option = Option(
        question_id=question.id,
        text=text,
        activates_contradiction=activates_contradiction,
        contradiction_code=contradiction_code,
        contradiction_penalty=contradiction_penalty,
    )
    db.add(option)
    db.commit()
    db.refresh(option)
    return option


def assign_option_effect(
    db: Session, *, option: Option, dimension: str, value: int
) -> OptionEffect:
    existing = db.scalar(
        select(OptionEffect).where(
            OptionEffect.option_id == option.id,
            OptionEffect.dimension == dimension,
        )
    )
    if existing:
        existing.value = value
        db.commit()
        db.refresh(existing)
        return existing

    effect = OptionEffect(option_id=option.id, dimension=dimension, value=value)
    db.add(effect)
    db.commit()
    db.refresh(effect)
    return effect


def assign_next_question(
    db: Session, *, option: Option, next_question: Question
) -> OptionNextQuestion:
    existing = db.scalar(
        select(OptionNextQuestion).where(OptionNextQuestion.option_id == option.id)
    )
    if existing:
        existing.next_question_id = next_question.id
        db.commit()
        db.refresh(existing)
        return existing

    link = OptionNextQuestion(option_id=option.id, next_question_id=next_question.id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link
