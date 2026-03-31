# /app/models/mixins.py
from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime

class TimestampMixin:
    __allow_unmapped__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())