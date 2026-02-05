from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class AiThresholds(Base):
    __tablename__ = "ai_thresholds"

    id: Mapped[int] = mapped_column(primary_key=True)
    text_threshold: Mapped[float] = mapped_column(Float, default=0.6)
    media_threshold: Mapped[float] = mapped_column(Float, default=0.6)
    uniqueness_threshold: Mapped[float] = mapped_column(Float, default=0.7)
