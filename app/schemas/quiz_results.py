from uuid import UUID

from pydantic import BaseModel


class UserAnswers(BaseModel):
    answer: str
    is_correct_answer: bool


class Question(BaseModel):
    name: str
    answer: UserAnswers


class UserSumbition(BaseModel):
    questions: list[Question]


class QuizResultsBase(BaseModel):
    results: list[UserSumbition]


class QuizResultsGet(QuizResultsBase):
    id: UUID


class QuizResultsCreate(QuizResultsBase):
    company_id: UUID
    ...
