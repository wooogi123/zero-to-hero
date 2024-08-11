from sqlalchemy import Identity, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime, timezone

from .common import Base


class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    is_done: Mapped[bool] = mapped_column(nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=(lambda _: datetime.now(timezone.utc)),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=(lambda _: datetime.now(timezone.utc)),
        onupdate=(lambda _: datetime.now(timezone.utc)),
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
