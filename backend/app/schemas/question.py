from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import Dimension


class QuestionCreate(BaseModel):
    text: str = Field(min_length=3, max_length=500)
    is_start: bool = False
    is_terminal: bool = False


class OptionCreate(BaseModel):
    text: str = Field(min_length=1, max_length=300)


class OptionEffectAssign(BaseModel):
    dimension: Dimension
    value: int = Field(ge=-3, le=3)


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
    text: str
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


class QuestionDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    is_start: bool
    is_terminal: bool
    created_at: datetime
    options: list[OptionDetail]
