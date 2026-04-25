from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import Dimension


class QuestionCreate(BaseModel):
    key: str | None = Field(default=None, min_length=1, max_length=80)
    text: str = Field(min_length=3, max_length=500)
    main_dimension: Dimension | None = None
    is_start: bool = False
    is_terminal: bool = False


class OptionCreate(BaseModel):
    text: str = Field(min_length=1, max_length=300)
    activates_contradiction: bool = False
    contradiction_code: str | None = Field(default=None, max_length=120)
    contradiction_penalty: int = Field(default=0, ge=-10, le=0)


class OptionEffectAssign(BaseModel):
    dimension: Dimension
    value: int = Field(ge=-10, le=6)


class OptionNextQuestionAssign(BaseModel):
    next_question_id: int


class OptionEffectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dimension: Dimension
    value: int


class QuestionListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str | None
    text: str
    main_dimension: Dimension | None
    is_start: bool
    is_terminal: bool
    created_at: datetime


class OptionDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    created_at: datetime
    effects: list[OptionEffectRead]
    next_question_id: int | None
    activates_contradiction: bool
    contradiction_code: str | None
    contradiction_penalty: int


class QuestionDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str | None
    text: str
    main_dimension: Dimension | None
    is_start: bool
    is_terminal: bool
    created_at: datetime
    options: list[OptionDetail]
