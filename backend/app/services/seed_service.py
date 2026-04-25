from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.option import Option
from app.models.question import Question
from app.services.admin_service import (
    assign_next_question,
    assign_option_effect,
    create_option,
    create_question,
)
from app.utils.seed_data import SEED_QUESTIONS


def seed_initial_data(db: Session) -> None:
    existing = db.scalar(select(Question.id).where(Question.key == "rel_inicio").limit(1))
    if existing:
        return

    question_map: dict[str, Question] = {}
    option_links: list[tuple[Option, str]] = []

    # Las preguntas se crean primero para poder resolver enlaces entre nodos
    # aunque una opcion apunte a una pregunta definida mas adelante.
    for item in SEED_QUESTIONS:
        question = create_question(
            db,
            key=item["key"],
            text=item["text"],
            main_dimension=item.get("main_dimension"),
            is_start=item.get("is_start", False),
            is_terminal=item.get("is_terminal", False),
        )
        question_map[item["key"]] = question

    # Luego se crean opciones, efectos ponderados y enlaces diferidos del grafo.
    for item in SEED_QUESTIONS:
        question = question_map[item["key"]]
        for option_data in item["options"]:
            option = create_option(
                db,
                question=question,
                text=option_data["text"],
                activates_contradiction=option_data.get("activates_contradiction", False),
                contradiction_code=option_data.get("contradiction_code"),
                contradiction_penalty=option_data.get("contradiction_penalty", 0),
            )
            for dimension, value in option_data["effects"].items():
                assign_option_effect(db, option=option, dimension=dimension, value=value)
            next_key = option_data.get("next")
            if next_key:
                option_links.append((option, next_key))

    for option, next_key in option_links:
        assign_next_question(db, option=option, next_question=question_map[next_key])
