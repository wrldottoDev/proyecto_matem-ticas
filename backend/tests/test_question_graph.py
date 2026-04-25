from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.core.enums import FinalResult
from app.db.base import Base
from app.models.option import Option
from app.models.question import Question
from app.services.seed_service import seed_initial_data
from app.services.session_service import answer_question, get_start_question, start_session


def make_db() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def choose_option(db: Session, question: Question, text_fragment: str) -> Option:
    for option in sorted(question.options, key=lambda item: item.id):
        if text_fragment in option.text:
            return option
    raise AssertionError(f"No option containing {text_fragment!r} for {question.key}")


def answer_by_text(db: Session, session_id: int, question: Question, text_fragment: str):
    option = choose_option(db, question, text_fragment)
    return answer_question(
        db,
        session_id=session_id,
        question_id=question.id,
        option_id=option.id,
    )


def test_seed_loads_directed_question_graph() -> None:
    db = make_db()
    seed_initial_data(db)

    questions = db.scalars(select(Question)).all()
    linked_options = db.scalars(
        select(Option).where(Option.next_question_link.has())
    ).all()
    contradiction_options = db.scalars(
        select(Option).where(Option.activates_contradiction.is_(True))
    ).all()

    assert len(questions) >= 20
    assert get_start_question(db).key == "rel_inicio"
    assert linked_options
    assert contradiction_options


def test_green_flag_route_finishes_high() -> None:
    db = make_db()
    seed_initial_data(db)
    session = start_session(db)
    question = get_start_question(db)

    for fragment in [
        "constante, clara",
        "directo incluso",
        "consistencia entre palabras",
        "sin presionar",
        "Respeta el límite",
        "sin controlar",
        "escucha, pregunta",
        "reconoce errores",
        "ambos cuidan",
        "puede vincularse",
        "intenta comprender",
        "presencia, acuerdos",
        "sano, recíproco",
    ]:
        payload = answer_by_text(db, session.id, question, fragment)
        if payload.session_finished:
            assert payload.result is not None
            assert payload.result.final_result == FinalResult.green_flag
            return
        assert payload.question is not None
        question = db.get(Question, payload.question.id)

    raise AssertionError("Green route did not finish")


def test_contradiction_route_records_penalty() -> None:
    db = make_db()
    seed_initial_data(db)
    session = start_session(db)
    question = get_start_question(db)

    for fragment in [
        "constante, clara",
        "justifica ocultar",
        "torcer los hechos",
        "suele distorsionar",
        "control, mentira",
        "compromete mi bienestar",
    ]:
        payload = answer_by_text(db, session.id, question, fragment)
        if payload.session_finished:
            assert payload.result is not None
            assert payload.result.final_result == FinalResult.red_flag
            assert payload.result.contradiction_count >= 1
            assert "honestidad_justifica_mentir" in payload.result.contradictions
            assert payload.result.raw_scores.confianza < 0
            return
        assert payload.question is not None
        question = db.get(Question, payload.question.id)

    raise AssertionError("Contradiction route did not finish")
