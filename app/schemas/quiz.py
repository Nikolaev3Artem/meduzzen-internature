from uuid import UUID

from pydantic import BaseModel, field_validator


class Answer(BaseModel):
    name: str
    is_correct: bool


class Question(BaseModel):
    name: str
    answers: list[Answer]


class QuizBase(BaseModel):
    name: str
    description: str


class QuizCreate(QuizBase):
    questions: list[Question]

    @field_validator("questions")
    @classmethod
    def more_than_two_check(cls, questions: list[Question]) -> list[Question]:
        if len(questions) < 2:
            raise ValueError("Questions must be more than two")
        return questions


class QuizUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    questions: list[Question] | None = None


class QuizGet(QuizBase):
    id: UUID
    questions: list[Question]
