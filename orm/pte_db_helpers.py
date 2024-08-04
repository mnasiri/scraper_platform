from sqlalchemy.orm import Session

# from . import models, schemas
from database.pte_db import Question


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Question).offset(skip).limit(limit).all()


def get_question(db: Session, q_id: str):
    """
    get shop by torob_id
    :param db:
    :param q_id:
    :return:
    """
    return db.query(Question).filter(Question.pte_id == q_id).first()


def create_question(db: Session, pte_id: str, transcript: str):
    db_city = Question(pte_id=pte_id, transcript=transcript)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city
