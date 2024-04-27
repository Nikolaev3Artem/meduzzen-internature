import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True


class IDBase(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )


class RequestStatus(enum.Enum):
    MEMBER = "Member"
    INVITATION = "Invitation"
    JOIN_REQUEST = "Join_Request"


class CompanyRequests(IDBase):
    __tablename__ = "company_requests"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    company_id: Mapped[UUID] = mapped_column(ForeignKey("company.id"))
    status: Mapped[Enum] = mapped_column(Enum(RequestStatus))


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
