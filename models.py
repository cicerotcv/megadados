from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True,
                        index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    annotation = Column(String, nullable=True)
    professor = Column(String, nullable=True)

    notes = relationship("Note", back_populates="owner")


class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(Float, index=True)
    subject = Column(Integer, ForeignKey('subjects.subject_id'))

    owner = relationship("Subject", back_populates="notes")
