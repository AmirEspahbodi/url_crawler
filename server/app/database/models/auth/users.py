import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import BIGINT, DATE

from app.core.connection.database import Base
from ..mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(64),
        nullable=True,
        default=None,
    )
    uuid: Mapped[str] = mapped_column(
        String(63),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    birthday: Mapped[datetime.date] = mapped_column(
        DATE,
        nullable=True,
        default=None,
    )
    is_active: Mapped[int] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    is_admin: Mapped[int] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    urls: Mapped[list["Url"]] = relationship(
        "Url",
        secondary="user_urls",
        primaryjoin="and_(User.id == UserUrl.user_id)",
        secondaryjoin="and_(UserUrl.url_id == Url.id, Url.is_deleted == False)",
        viewonly=True,
    )
