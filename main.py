# coding utf-8

from os import name
from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from fastapi.param_functions import Path
from fastapi.params import Body, Param
from models import AddNote, Note, SubjectIn, SubjectOut
# substituir ao implementar a conexao com o banco de dados
from utils import dummy_database as db


app = FastAPI()


@app.get("/")
async def root():
    return {"app": "megadados"}


@app.post('/subject', response_model=SubjectOut, name="Create subject")
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


@app.get('/subject', response_model=List[str], name="List all subjects names")
async def list_subject_name():
    return [subject['name'] for subject in db.list()]


@app.get('/subjects', response_model=List[SubjectOut], name="List all subjects")
async def list_subjects():
    return db.list()


@app.delete('/subject/{subject_id}', response_model=None)
async def delete_subject(
        subject_id: UUID = Path(
            ..., example="69c880b4-ae6c-4c85-832d-420124e50fde"
        )):
    db.delete_by_id(subject_id)


@app.patch('/subject/{subject_id}', response_model=SubjectOut)
async def update_subject(
        subject_id: UUID = Path(
            ..., example="69c880b4-ae6c-4c85-832d-420124e50fde"
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


@app.post('/note/{subject_id}', response_model=List[Note])
async def add_note(
    subject_id: UUID = Path(
        ...,
        example="1e3f4915-d9a5-4777-9d43-11e21b4f296f"
    ),
    body: AddNote = Body(
        ...,
        example={"note": 5}
    )
):

    subject_exists = db.has(str(subject_id))
    if not subject_exists:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    subject_notes = db.insert_note(subject_id, body.note)

    return subject_notes


@app.delete('/note/{subject_id}/{note_id}', response_model=None)
async def delete_note(
        subject_id: UUID = Path(
            ...,
            example="69c880b4-ae6c-4c85-832d-420124e50fde"
        ),
        note_id: UUID = Path(
            ...,
            example="c89d13ca-0ca2-4d12-a4e5-099019584024"
        )):
    subject_exists = db.has(str(subject_id))

    if not subject_exists:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    db.delete_note(str(subject_id), str(note_id))


@app.get('/note/{subject_id}', response_model=List[Note])
async def list_notes(
        subject_id: UUID = Path(
            ...,
            example="69c880b4-ae6c-4c85-832d-420124e50fde"
        )):
    subject = db.find_by_id(str(subject_id))

    if not subject:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    return subject['notes']


@app.patch('/note/{subject_id}/{note_id}', response_model=List[Note])
async def update_note(
        subject_id: UUID = Path(
            ...,
            example="69c880b4-ae6c-4c85-832d-420124e50fde"
        ),
        note_id: UUID = Path(
            ...,
            example="c89d13ca-0ca2-4d12-a4e5-099019584024"
        ),
        data: AddNote = Body(
            ...,
            example={
                'note': 5.6
            }
        )):
    subject_exists = db.has(str(subject_id))

    if not subject_exists:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    updated_notes = db.update_note(str(subject_id), str(note_id), data.note)
    return updated_notes
