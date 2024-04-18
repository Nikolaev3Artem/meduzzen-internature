import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from db.postgress import metadata


class Base(DeclarativeBase):
    __abstract__ = True
    metadata


class IDBase(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class User(IDBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(80), unique=True)
    password: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String(100))
