from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True,
                        index=True, autoincrement=True)
    name = Column(String(40), unique=True, index=True)
    annotation = Column(String(100), nullable=True)
    professor = Column(String(30), nullable=True)

    notes = relationship("Note", back_populates="owner",  cascade="all, delete-orphan")


class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(Float, index=True)
    subject = Column(Integer, ForeignKey('subjects.subject_id'))

    owner = relationship("Subject", back_populates="notes")
