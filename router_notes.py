
from fastapi import HTTPException, APIRouter
from fastapi.params import Body, Path
from typing import List
from uuid import UUID
from models import AddNote, Note

# substituir ao implementar a conexao com o banco de dados
from utils import dummy_database as db

router = APIRouter(prefix='/note', tags=['notes'])


@router.post('/{subject_id}', response_model=List[Note])
async def add_note(
    subject_id: UUID = Path(
        ...,
        example="08c4ff5e-a854-4a4b-833a-211dd77fc6da"
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


@router.delete('/{subject_id}/{note_id}', response_model=None)
async def delete_note(
        subject_id: UUID = Path(
            ...,
            example="08c4ff5e-a854-4a4b-833a-211dd77fc6da"
        ),
        note_id: UUID = Path(
            ...,
            example="03401e80-4d71-415f-9146-5ef734a5c22d"
        )):
    subject_exists = db.has(str(subject_id))

    if not subject_exists:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    note_exists = db.has_note(str(subject_id), str(note_id))
    if not note_exists:
        raise HTTPException(
            404, detail=f"Note with id '{note_id}' does not exist in the subject with id '{subject_id}'")

    db.delete_note(str(subject_id), str(note_id))


@router.get('/{subject_id}', response_model=List[Note])
async def list_notes(
        subject_id: UUID = Path(
            ...,
            example="08c4ff5e-a854-4a4b-833a-211dd77fc6da"
        )):
    subject = db.find_by_id(str(subject_id))

    if not subject:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    return subject['notes']


@router.patch('/{subject_id}/{note_id}', response_model=List[Note])
async def update_note(
        subject_id: UUID = Path(
            ...,
            example="08c4ff5e-a854-4a4b-833a-211dd77fc6da"
        ),
        note_id: UUID = Path(
            ...,
            example="03401e80-4d71-415f-9146-5ef734a5c22d"
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

    note_exists = db.has_note(str(subject_id), str(note_id))
    if not note_exists:
        raise HTTPException(
            404, detail=f"Note with id '{note_id}' does not exist in the subject with id '{subject_id}'")

    updated_notes = db.update_note(str(subject_id), str(note_id), data.note)
    return updated_notes
