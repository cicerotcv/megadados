from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Depends, Path
from sqlalchemy.orm.session import Session

import crud
from database import get_db
from schemas import SubjectOut

router = APIRouter(prefix='/subject', tags=['subjects'])


@router.post('', response_model=SubjectOut, name="Create subject")
async def create_subject(
    subject: SubjectOut = Body(
        ...,
        example={
            "name": "Microdados",
            "annotation": "Disciplina cheia de atividades",
            "professor": "Fabio Toshimoto"
        }
    ),
    db: Session = Depends(get_db)
):

    subject_exists = crud.find_subject(db,  name=subject.name)

    if subject_exists:
        raise HTTPException(
            status_code=400, detail=f"Subject with name '{subject.name}' already exists")

    return crud.create_subject(db=db, subject=subject)


@router.get('', response_model=List[str], name="List all subjects names")
async def list_subject_name(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    subjects = crud.get_subjects_names(db=db, limit=limit, skip=skip)

    return [subject.name for subject in subjects]


@router.get('/list', response_model=List[SubjectOut], name="List all subjects")
async def list_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subjects = crud.get_subjects(db, skip=skip, limit=limit)
    return subjects


@router.delete('/{subject_id}', response_model=None)
async def delete_subject_by_id(
        subject_id: int = Path(
            ..., example=3
        ),
        db: Session = Depends(get_db)):

    crud.delete_subject_by_id(db, subject_id=subject_id)


@router.patch('/{subject_id}', response_model=SubjectOut)
async def update_subject(
        subject_id: int = Path(
            ..., example=3
        ),
        subject: SubjectOut = Body(
            ..., example={
                "name": "Microdados",
                "annotation": "Disciplina cheia de atividades",
                "professor": "Fabio Toshimoto"
            }
        ),
        db: Session = Depends(get_db)):

    old = crud.find_subject_by_id(db, subject_id)

    if not old:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' not found")

    name_has_changed = subject.name != old.name

    if name_has_changed:
        # verificar se existe outra disciplina com o nome escolhido
        another_subject = crud.find_subject(db, subject.name)
        name_is_duplicated = another_subject and another_subject.subject_id != subject.subject_id
        if name_is_duplicated:
            raise HTTPException(
                400, detail=f"Subject with name '{subject.name}' already exists")

    new = crud.update_subject_by_id(db, subject_id=subject_id, subject=subject)

    return new
