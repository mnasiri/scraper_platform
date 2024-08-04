from sqlalchemy import Column, Integer, String

from database import Base


class Question(Base):
    __tablename__ = "pte_questions"

    id = Column(Integer, primary_key=True)
    pte_id = Column(String, unique=True, index=True)
    transcript = Column(String, )
    