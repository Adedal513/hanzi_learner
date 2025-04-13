from sqlalchemy import Column, Integer, String
from services.db_service import Base


class Hanzi(Base):
    __tablename__ = 'hanzi'

    id = Column(Integer, primary_key=True)
    character = Column(String(1), unique=True, nullable=False)
    pinyin = Column(String(50), nullable=False)
    meaning = Column(String(100), nullable=False)
    s3_image_key = Column(String(200), nullable=False)

    def __repr__(self):
        return f"<Hanzi {self.character}"