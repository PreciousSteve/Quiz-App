# quiz app
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
    

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool   
    
class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get('/questions/{question_id}')
def read_question(question_id:int, session=Depends(get_db)):
    result = session.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='question id not found')
    return result


@app.get('/choices/{question_id}')
def read_choices(question_id:int, session=Depends(get_db)):
    result = session.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='choice not found')
    return result



@app.post('/questions')
def create_question(question:QuestionBase, session=Depends(get_db)):
    db_question = models.Questions(question_text=question.question_text)
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct =choice.is_correct, question_id=db_question.id)
        session.add(db_choice)
    session.commit()