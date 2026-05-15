from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.db.session import Base


class ConversionHistory(Base):
    __tablename__ = "conversion_history"

    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String(16), nullable=False)  # stt or tts
    input_path = Column(String(512), nullable=True)
    output_path = Column(String(512), nullable=True)
    transcript = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    voice = Column(String(128), nullable=True)
    rate = Column(Float, nullable=True)
    pitch = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
