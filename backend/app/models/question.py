from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    key: Mapped[str | None] = mapped_column(String(80), unique=True, nullable=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    main_dimension: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_start: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_terminal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")
    session_answers = relationship("SessionAnswer", back_populates="question")
