from sqlalchemy.orm import Session

import models
import schemas


def find_subject_by_id(db: Session, subject_id: int):
    """Encontra na tabela de "subjects" alguma linha com o subject_id corresponde

    Args:
        db (Session): objeto de session do database
        subject_id (int): id da discipla a ser localizada

    Returns:
        Subject | None: devolve a correspondência se houver, caso contrário, None;
    """
    return db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()


def find_subject(db: Session, name: str):
    """Encontra na tabela de "subjects" alguma linha com a propriedade "name" corresponde 

    Args:
        db (Session): objeto de session do database
        name (str): nome da disciplina

    Returns:
        Subject | None: devolve a correspondência se houver, caso contrário, None;
    """
    return db.query(models.Subject).filter(models.Subject.name == name).first()


def get_subjects_names(db: Session, limit: int, skip: int):
    """Busca a lista de todas as disciplinas no banco de dados

    Args:
        db (Session): objeto de session do database
        limit (int): número máximo de respostas esperada
        skip (int): offest do resultado

    Returns:
        List[str]: lista de nomes de disciplinas
    """
    return db.query(models.Subject).limit(limit).offset(skip).all()


def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    """Lista disciplinas

    Args:
        db (Session): objeto de session do database
        skip (int, optional): offset da busca. Por padrão é 0.
        limit (int, optional): limite de itens a serem baixados. Por padrão é 100.

    Returns:
        List[Subject]: lsita de resultados
    """
    return db.query(models.Subject).offset(skip).limit(limit).all()


def create_subject(db: Session, subject: schemas.SubjectIn):
    """Cria disciplina

    Args:
        db (Session): objeto de session do database
        subject (schemas.SubjectIn): objeto contendo as informações necessárias para criar uma disciplina

    Returns:
        Subject: disciplina criada
    """
    db_subject = models.Subject(
        name=subject.name, annotation=subject.annotation, professor=subject.professor)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def update_subject_by_id(db: Session, subject: schemas.SubjectOut, subject_id: int):
    """Atualiza uma disciplina a partir do id

    Args:
        db (Session): objeto de session do database
        subject (schemas.SubjectIn): objeto contendo as informações necessárias para atualizar a disciplina
        subject_id (int): id da disciplina

    Returns:
        Subject: disciplina atualizada
    """
    subject_data = subject.dict()
    subject_data["subject_id"] = subject_id

    del(subject_data['notes'])

    db.query(models.Subject).filter(models.Subject.subject_id ==
                                    subject_id).update(subject_data, synchronize_session="fetch")
    db.commit()
    return subject_data


def delete_subject_by_id(db: Session, subject_id: int):
    """Deleta uma uma disciplina do banco de dados

    Args:
        db (Session): objeto de session do database
        subject_id (int): id da disciplina 
    """
    subject = find_subject_by_id(db, subject_id)

    if subject:
        db.delete(subject)
        db.commit()


def get_notes(db: Session, subject_id: int, skip: int = 0, limit: int = 100):
    """Lista notas de uma disciplina

    Args:
        subject_id (int): id da disciplina 
        db (Session): objeto de session do database
        skip (int, optional): offset da busca. Por padrão é 0.
        limit (int, optional): limite de itens a serem baixados. Por padrão é 100.

    Returns:
        List[Note]: lista de resultados
    """
    return db.query(models.Note).filter(models.Note.subject == subject_id).offset(skip).limit(limit).all()


def find_note(db: Session, subject_id: int, note_id: int):
    """Encontra na tabela de "notes" alguma linha com o note_id e subject_id corresponde

    Args:
        db (Session): objeto de session do database
        note_id (int): id da nota da disciplina
        subject_id (int): id da disciplina 

    Returns:
        Note | None: nota localizada
    """
    return db.query(models.Note).filter(models.Note.subject == subject_id, models.Note.note_id == note_id).first()


def find_note_by_id(db: Session, note_id: int):
    """Encontra na tabela de "notes" alguma linha com o note_id corresponde

    Args:
        db (Session): objeto de session do database
        note_id (int): id da nota da disciplina

    Returns:
        Note | None: nota localizada
    """
    return db.query(models.Note).filter(models.Note.note_id == note_id).first()


def create_subject_note(db: Session, subject_id: int, note: schemas.Note):
    """Adiciona uma nota a uma disciplina

    Args:
        db (Session): objeto de session do database
        subject_id (int): id da disciplina 
        note (schemas.Note): objeto contendo o valor da nota

    Returns:
        Note: nota criada
    """
    db_note = models.Note(value=note, subject=subject_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note_by_id(db: Session, note: schemas.Note, note_id: int):
    """Atualiza uma nota pelo id

    Args:
        db (Session): objeto de session do database
        note (schemas.Note): objeto contendo o valor da nota
        note_id (int): id da nota a ser atualizada

    Returns:
        Note: nota atualizada
    """
    note_data = note.dict()

    note_data['value'] = note_data['note']

    del(note_data['note'])

    db.query(models.Note).filter(models.Note.note_id == note_id).update(
        note_data, synchronize_session="fetch")
    db.commit()
    return find_note_by_id(db, note_id)


def delete_note_by_id(db: Session, note_id: int):
    """Deleta uma nota pelo id

    Args:
        db (Session): objeto de session do database
        note_id (int): id da nota a ser deletada
    """
    note = find_note_by_id(db, note_id)

    if note:
        db.delete(note)
        db.commit()
