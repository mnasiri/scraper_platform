import logging
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api import app, get_db
from database.pte_db import Question
from orm.pte_db_helpers import get_question, create_question, get_questions
from run_playwright_sample.pte_get_question_info import get_question_transcript

logger = logging.getLogger(__file__)



@app.get("/pte/questions/")
async def read_shops(skip: int = 0, limit: int = 10, search: Optional[str] = None, db: Session = Depends(get_db)):
    items = get_questions(db=db, skip=skip, limit=limit)
    return {"items": items, "skip": skip, "limit": limit}


@app.get('/pte/questions/{id}')
async def read_question(id: str, search: Optional[str] = None, db: Session = Depends(get_db)):
    question_data = get_question(db=db, q_id=id)

    if not question_data:
        raise HTTPException(status_code=404, detail="question not found")
    return question_data


@app.get('/pte/questions/{id}/gather')
async def gather_a_question(id: str, search: Optional[str] = None, db: Session = Depends(get_db)):
    return await gather_question(db, id)


@app.get('/pte/questions/gather/{from_id}/{to_id}')
async def gather_questions(from_id: int, to_id: int, search: Optional[str] = None, db: Session = Depends(get_db)):
    counter = 0
    for id in range(from_id, to_id):
        if id % 20 > 18:
            print(f'the {id} question gathered ')
        try:
            data = await gather_question(db, str(id), is_raise_exception=False)
        except Exception:
            print(f'error in gather in for {id}')
            continue
        if data:
            counter += 1

    return {'counter': counter}


async def gather_question(db: Session, id: str, is_raise_exception: bool = True):
    question_data = get_question(db=db, q_id=id)
    if not question_data:
        transcript = await get_question_transcript(q_id=id)
    else:
        transcript = question_data.get('transcript')

    if not transcript:
        if is_raise_exception:
            raise HTTPException(status_code=404, detail=f"question not found {id}")
        return question_data

    db_question: Question = create_question(db, pte_id=id, transcript=transcript)

    if not db_question:
        if is_raise_exception:
            raise HTTPException(status_code=404, detail=f"question not found {id}")
        return db_question

    return question_data
