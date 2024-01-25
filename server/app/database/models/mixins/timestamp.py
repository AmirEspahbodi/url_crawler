# pylint: skip-file
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import TIMESTAMP, BOOLEAN
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            TIMESTAMP,
            default=func.now(),
            nullable=False,
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            TIMESTAMP,
            default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )

    @declared_attr
    def deleted_at(cls) -> Mapped[datetime]:
        return mapped_column(
            TIMESTAMP,
            nullable=True,
        )

    @declared_attr
    def is_deleted(cls) -> Mapped[bool]:
        return mapped_column(
            BOOLEAN,
            nullable=False,
            default=False,
        )
