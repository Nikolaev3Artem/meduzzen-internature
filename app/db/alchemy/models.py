import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True


class IDBase(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
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

    owner_id: Mapped[int] = mapped_column(UUID(as_uuid=True), nullable=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    visible: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
