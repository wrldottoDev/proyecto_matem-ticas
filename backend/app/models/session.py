from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    final_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    final_result: Mapped[str | None] = mapped_column(String(50), nullable=True)

    answers = relationship("SessionAnswer", back_populates="session", cascade="all, delete-orphan")


class SessionAnswer(Base):
    __tablename__ = "session_answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    option_id: Mapped[int] = mapped_column(ForeignKey("options.id", ondelete="CASCADE"), nullable=False)
    answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    session = relationship("Session", back_populates="answers")
    question = relationship("Question", back_populates="session_answers")
    option = relationship("Option", back_populates="session_answers")
