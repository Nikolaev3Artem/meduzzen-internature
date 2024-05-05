from uuid import UUID

from pydantic import BaseModel


class UserAnswers(BaseModel):
    question: str
    is_correct_answer: bool


class UserSumbition(BaseModel):
    answers: list[UserAnswers]


class QuizResultsBase(BaseModel):
    results: list[UserSumbition]


class QuizResultsGet(QuizResultsBase):
    id: UUID


class QuizResultsCreate(QuizResultsBase):
    ...
