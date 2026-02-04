from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database import Base

class Summary(Base):
    __tablename__ = 'summaries'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_content: Mapped[str] = mapped_column(Text, nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Summary(id={self.id}, create_at{self.created_at})>'