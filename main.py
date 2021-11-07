# coding utf-8

from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from models import SubjectIn, SubjectOut


app = FastAPI()


subjects = [{
    "subject_id": "08c4ff5e-a854-4a4b-833a-211dd77fc6da",
    "name": "Microdados",
    "annotation": "Disciplina de banco de dados",
    "professor": "Fabio Toshimoto",
    "notes": []
}]


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

    already_exists = len([
        item for item in subjects if item["name"] == subject.name
    ]) > 0

    if already_exists:
        raise HTTPException(
            status_code=400, detail=f"Subject with name '{subject.name}' already exists")

    subject_dict = subject.dict()
    subject_dict.update({"subject_id": uuid4()})
    subjects.append(subject_dict)

    return subject_dict


# O usuário pode listar os nomes de suas disciplinas
@app.get('/subject', response_model=List[SubjectOut])
async def list_subjects():
    return subjects


# O usuário pode deletar uma disciplina
@app.delete('/subject/{subject_id}')
async def delete_subject(subject_id: UUID):
    global subjects
    subjects = [
        subject for subject in subjects if subject['subject_id'] != str(subject_id)]


# O usuário pode modificar as informações de uma disciplina INCLUINDO seu nome
@app.patch('/subject/{subject_id}', response_model=SubjectOut)
async def update_subject(subject_id: UUID, subject: SubjectIn):
    # name, annotation, professor, notes
    subject_dict = subject.dict()

    pass

    # O usuário pode adicionar uma nota a uma disciplina
    # O usuário pode deletar uma nota de uma disciplina
    # O usuário pode listar as notas de uma disciplina
    # O usuário pode modificar uma nota de uma disciplina
