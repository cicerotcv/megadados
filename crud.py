from sqlalchemy.orm import Session

import models
import schemas


def find_subject_by_id(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()


def find_subject(db: Session, name: str):
    return db.query(models.Subject).filter(models.Subject.name == name).first()


def get_subjects_names(db: Session, limit: int, skip: int):
    return db.query(models.Subject).limit(limit).offset(skip).all()


def find_note_by_id(db: Session, note_id: int):

    return db.query(models.Note).filter(models.Note.note_id == note_id).first()


def get_subjects(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Subject).offset(skip).limit(limit).all()


def get_notes(db: Session, subject_id: int, skip: int = 0, limit: int = 100):

    return db.query(models.Note).filter(models.Note.subject == subject_id).offset(skip).limit(limit).all()


def create_subject(db: Session, subject: schemas.SubjectIn):
    db_subject = models.Subject(
        name=subject.name, annotation=subject.annotation, professor=subject.professor)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def create_subject_note(db: Session, subject_id: int, note: schemas.Note):
    db_note = models.Note(value=note, subject=subject_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_subject_by_id(db: Session, subject: schemas.SubjectOut, subject_id: int):
    subject_data = subject.dict()
    subject_data["subject_id"] = subject_id

    del(subject_data['notes'])

    db.query(models.Subject).filter(models.Subject.subject_id ==
                                    subject_id).update(subject_data, synchronize_session="fetch")
    db.commit()
    return subject_data


def update_note_by_id(db: Session, note: schemas.Note, note_id: int):
    note_data = note.dict()

    note_data['value'] = note_data['note']

    del(note_data['note'])

    db.query(models.Note).filter(models.Note.note_id == note_id).update(
        note_data, synchronize_session="fetch")
    db.commit()
    return note_data


def delete_subject_by_id(db: Session, subject_id: int):
    subject = find_subject_by_id(db, subject_id)

    if subject:
        db.delete(subject)
        db.commit()


def delete_note_by_id(db: Session, note_id: int):
    note = find_note_by_id(db, note_id)

    if note:
        db.delete(note)
        db.commit()
