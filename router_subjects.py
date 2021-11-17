from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Depends, Path
from typing import List

from sqlalchemy.orm.session import Session
from schemas import SubjectIn, SubjectOut

# substituir ao implementar a conexao com o banco de dados
# from utils import dummy_database as db
from database import get_db
import crud

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
    db_subject = crud.find_subject_by_id(db, subject_id=subject.subject_id)

    # already_exists = db.has(value=subject.name, key='name')

    if db_subject:
        raise HTTPException(
            status_code=400, detail=f"Subject with name '{subject.name}' already exists")

    # subject_dict = subject.dict()
    # db.insert(subject_dict)

    return crud.create_subject(db=db, subject=subject)


# @router.get('', response_model=List[str], name="List all subjects names")
# async def list_subject_name():
#     return [subject['name'] for subject in db.list()]


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

    # old = db.find_by_id(subject_id)

    old = crud.find_subject_by_id(db, subject_id)

    if not old:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' not found")

    # valida alterações de nome
    # se já existe alguma disciplina com esse nome e se a
    # disciplina nao for a que está sendo alterada, devemos retornar um erro
    # if db.has(subject.name, 'name') and old["name"] != subject.name:
    #     raise HTTPException(
    #         400, detail=f"Subject with name '{subject.name}' already exists")

    new = crud.update_subject_by_id(db,subject_id = subject_id, subject = subject)

    return new
