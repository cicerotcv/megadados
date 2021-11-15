from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base

class Subject(Base):
    __tablename__ = "subjects"

    subject_id=Column(Integer, primary_key=True, index=True)
    name=Column(String, unique=True, index=True)
    annotation=Column(String, nullable=True)
    professor=Column(String, nullable=True)
    
    notes = relationship("Item", back_populates="owner")


class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, index=True)
    subject = Column(String, ForeignKey('subject.subject_id'))

    owner = relationship("Subject", back_populates="notes")
