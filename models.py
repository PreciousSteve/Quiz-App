from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from database import Base


class Questions(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True)
    question_text = Column(String)
    
    
class Choices(Base):
    __tablename__ = 'choices'
    
    id = Column(Integer, primary_key=True)
    choice_text = Column(String)
    is_correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey("questions.id"))
