from datetime import datetime
from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Memes(Base):
    __tablename__ = "memes"
    __table_args__ = {'extend_existing': True}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    bucket_name: str = Column(String, nullable=True)
    object_name: str = Column(String, nullable=True)
    date_of_addition: datetime.utcnow = Column(TIMESTAMP, default=datetime.utcnow())  # дата добавления мема
