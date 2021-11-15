from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Path
from typing import List
from uuid import UUID
from schemas import SubjectIn, SubjectOut

# substituir ao implementar a conexao com o banco de dados
from utils import dummy_database as db


router = APIRouter(prefix='/subject', tags=['subjects'])


@router.post('', response_model=SubjectOut, name="Create subject")
async def create_subject(
    subject: SubjectIn = Body(
        ...,
        example={
            "name": "Microdados",
            "annotation": "Disciplina cheia de atividades",
            "professor": "Fabio Toshimoto"
        }
    )
):

    already_exists = db.has(value=subject.name, key='name')

    if already_exists:
        raise HTTPException(
            status_code=400, detail=f"Subject with name '{subject.name}' already exists")

    subject_dict = subject.dict()
    db.insert(subject_dict)

    return subject_dict


@router.get('', response_model=List[str], name="List all subjects names")
async def list_subject_name():
    return [subject['name'] for subject in db.list()]


@router.get('/list', response_model=List[SubjectOut], name="List all subjects")
async def list_subjects():
    return db.list()


@router.delete('/{subject_id}', response_model=None)
async def delete_subject(
        subject_id: UUID = Path(
            ..., example="08c4ff5e-a854-4a4b-833a-211dd77fc6da"
        )):
    db.delete_by_id(subject_id)


@router.patch('/{subject_id}', response_model=SubjectOut)
async def update_subject(
        subject_id: UUID = Path(
            ..., example="08c4ff5e-a854-4a4b-833a-211dd77fc6da"
        ),
        subject: SubjectIn = Body(
            ..., example={
                "name": "Microdados",
                "annotation": "Disciplina cheia de atividades",
                "professor": "Fabio Toshimoto"
            }
        )):

    old = db.find_by_id(subject_id)
    if not old:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' not found")

    # valida alterações de nome
    # se já existe alguma disciplina com esse nome e se a
    # disciplina nao for a que está sendo alterada, devemos retornar um erro
    if db.has(subject.name, 'name') and old["name"] != subject.name:
        raise HTTPException(
            400, detail=f"Subject with name '{subject.name}' already exists")

    new = db.update_by_id(subject_id, subject.dict())
    return new
