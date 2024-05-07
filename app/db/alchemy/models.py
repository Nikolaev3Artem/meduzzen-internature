import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True


class IDBase(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )


class User(IDBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)


class Company(IDBase):
    __tablename__ = "company"

    owner_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    visible: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)


class CompanyRequests(IDBase):
    __tablename__ = "company_requests"

    user_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE")
    )
    company_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("company.id", ondelete="CASCADE")
    )
    status: Mapped[Enum] = mapped_column(
        ENUM("member", "invitation", "join_request", "admin", name="user_status")
    )


class Quiz(IDBase):
    __tablename__ = "quiz"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    submitions: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    questions: Mapped[JSONB] = mapped_column(JSONB(), nullable=False)
    company_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )


class QuizResults(IDBase):
    __tablename__ = "quiz_results"

    company_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    quiz_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    results: Mapped[JSONB] = mapped_column(JSONB(), nullable=True)
