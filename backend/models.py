from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Voice_Line(Base):
    __tablename__ = "embedded_voice_lines"

    ID: Mapped[str] = mapped_column(String, primary_key=True, index=True) 
    hero: Mapped[str] = mapped_column(String, nullable=False, index=True)
    line: Mapped[str] = mapped_column(String, nullable=False)
    audio_url: Mapped[str | None] = mapped_column(String, nullable=True) 
    embedding: Mapped[list[float] | None] = mapped_column(JSON, nullable=True)
    

    
