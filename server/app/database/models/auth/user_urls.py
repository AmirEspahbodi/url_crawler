from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT

from app.core.connection.database import Base


class UserUrl(Base):
    __tablename__ = "user_urls"

    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )
    url_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("urls.id"),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("users.id"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        default=False,
    )
