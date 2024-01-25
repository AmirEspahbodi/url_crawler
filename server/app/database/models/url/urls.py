from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Index, INTEGER
from sqlalchemy.dialects.postgresql import BIGINT, TEXT
from sqlalchemy.schema import UniqueConstraint

from app.core.connection.database import Base
from ..mixins import TimestampMixin


class Url(Base, TimestampMixin):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )
    domain: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )
    path: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,
        default=None,
    )
    query_string: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,
        default=None,
    )
    fragment: Mapped[str] = mapped_column(
        TEXT,
        nullable=True,
        default=None,
    )

    title: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    icon: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    crawl_times: Mapped[int] = mapped_column(
        INTEGER,
        nullable=False,
        default=1,
    )

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_urls",
        primaryjoin="and_(Url.id == UserUrl.url_id)",
        secondaryjoin="and_(User.id == UserUrl.user_id, User.is_deleted == False)",
        viewonly=True,
    )

    __table_args__ = (
        # UniqueConstraint(
        #     "domain",
        #     "path",
        #     "query_string",
        #     "fragment",
        #     name="unique_url",
        # ),
        Index(
            "urls_index",
            "domain",
            "path",
            "query_string",
            "fragment",
        ),
    )
