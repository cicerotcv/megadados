# coding utf-8

from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from models import SubjectIn, SubjectOut
# substituir ao implementar a conexao com o banco de dados
from utils import dummy_database as db


app = FastAPI()


@app.get("/")
async def root():
    return {"app": "megadados"}


# O usuário pode criar uma disciplina
# A disciplina tem um nome único (obrigatório)
# A disciplina tem um nome de professor (opcional)
# A disciplina tem um campo de anotação livre (texto)
@app.post('/subject', response_model=SubjectOut)
async def create_subject(
    subject: SubjectIn = Body(
        ...,
        examples={
            "normal": {
                "name": "Microdados",
                "annotation": "Disciplina cheia de atividades",
                "professor": "Fabio Toshimoto",
                "notes": [3.4, 6.6]
            },
            "wrong": {
                "name": 1234,
                "annotation": "example of note",
                "professor": "jhon doe",
                "notes": "nota"
            },
        },
    )
):

    already_exists = db.has(value=subject.name, key='name')

    if already_exists:
        raise HTTPException(
            status_code=400, detail=f"Subject with name '{subject.name}' already exists")

    subject_dict = subject.dict()
    db.insert(subject_dict)

    return subject_dict


# O usuário pode listar os nomes de suas disciplinas
@app.get('/subject', response_model=List[SubjectOut])
async def list_subjects():
    return db.list()


# O usuário pode deletar uma disciplina
@app.delete('/subject/{subject_id}')
async def delete_subject(subject_id: UUID):
    db.delete_by_id(subject_id)


# O usuário pode modificar as informações de uma disciplina INCLUINDO seu nome
@app.patch('/subject/{subject_id}', response_model=SubjectOut)
async def update_subject(subject_id: UUID, subject: SubjectIn):
    # name, annotation, professor, notes

    old = db.find_by_id(subject_id)
    if not old:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' not found")

    # valida alterações de nome
    # se já existe alguma disciplane com esse nome e se a
    # disciplina nao for a que está sendo alterada, devemos retornar um erro
    if db.has(subject.name, 'name') and old["name"] != subject.name:
        raise HTTPException(
            400, detail=f"Subject with name '{subject.name}' already exists")

    new = db.update_by_id(subject_id, subject.dict())
    return new

    # O usuário pode adicionar uma nota a uma disciplina
    # O usuário pode deletar uma nota de uma disciplina
    # O usuário pode listar as notas de uma disciplina
    # O usuário pode modificar uma nota de uma disciplina
