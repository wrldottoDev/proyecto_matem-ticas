from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Dimension
from app.models.base import Base


class Option(Base):
    __tablename__ = "options"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(String(300), nullable=False)
    activates_contradiction: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    contradiction_code: Mapped[str | None] = mapped_column(String(120), nullable=True)
    contradiction_penalty: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    question = relationship("Question", back_populates="options")
    effects = relationship("OptionEffect", back_populates="option", cascade="all, delete-orphan")
    next_question_link = relationship(
        "OptionNextQuestion", back_populates="option", cascade="all, delete-orphan", uselist=False
    )
    session_answers = relationship("SessionAnswer", back_populates="option")


class OptionEffect(Base):
    __tablename__ = "option_effects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    option_id: Mapped[int] = mapped_column(ForeignKey("options.id", ondelete="CASCADE"), nullable=False)
    dimension: Mapped[Dimension] = mapped_column(String(50), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)

    option = relationship("Option", back_populates="effects")


class OptionNextQuestion(Base):
    __tablename__ = "option_next_questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    option_id: Mapped[int] = mapped_column(
        ForeignKey("options.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    next_question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )

    option = relationship("Option", back_populates="next_question_link")
    next_question = relationship("Question")
