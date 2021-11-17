from re import sub
from sqlalchemy.orm import Session

import models, schemas


def find_subject_by_id(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()


def find_note_by_id(db: Session, note_id: int):

    return db.query(models.Note).filter(models.Note.note_id == note_id).first()


def get_subjects(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Subject).offset(skip).limit(limit).all()

def get_notes(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Note).offset(skip).limit(limit).all()


def create_subject(db: Session, subject: schemas.SubjectIn):
    db_subject = models.Subject(name=subject.name, annotation=subject.annotation, professor=subject.professor)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def create_subject_note(db: Session, note: schemas.AddNote, subject_id: int):
    db_note = models.Note(**note.dict(), owner_id=subject_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_subject_by_id(db: Session, subject: schemas.SubjectOut, subject_id: int):
    subject_data = subject.dict()
    subject_data["subject_id"] = subject_id

    del(subject_data['notes'])

    db.query(models.Subject).filter(models.Subject.subject_id == subject_id).update(subject_data, synchronize_session="fetch")
    db.commit()
    return subject_data

def update_note_by_id(db: Session, note: schemas.Note, note_id: int):
    db_note = models.Note(**note.dict())
    db.query(models.Note).filter(models.Note.note_id == note_id).update(db_note, synchronize_session="fetch")
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_subject_by_id(db: Session, subject_id: int):
    # db_subject = models.Subject(subject_id = subject_id)
    subject = find_subject_by_id(db, subject_id)

    if subject:
        db.delete(subject)
        db.commit()

def delete_note_by_id(db: Session, note_id: int):
    db_note = models.Note(note_id = note_id)
    db.delete(db_note)
    db.commit()

