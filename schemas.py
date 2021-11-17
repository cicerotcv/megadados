from typing import List, Optional
from pydantic import BaseModel
from pydantic.fields import Field

NoteValidator = Field(..., ge=0, le=10, description="User note for a subject")

SubjectNameValidator = Field(..., title="Subject Name",
                             description="Name of this subject (must be unique)",  min_length=0, max_length=40)

SubjectAnnotationValidator = Field(None, title="Subject Annotation",
                                   description="Optional annotation for this subject", max_length=100)

SubjectProfessorValidator = Field(None, title="Subject Professor",
                                  description="Professor name of this subject", max_length=30)

SubjectNotesValidator = Field([], title="Subject Notes",
                              description="Tests and homeworks scores of this subject")


class AddNote(BaseModel):
    note: float = NoteValidator


class Note(BaseModel):
    note_id: int
    value: float = NoteValidator
    subject: int

    class Config:
        orm_mode = True

class SubjectIn(BaseModel):
    name: str = SubjectNameValidator
    annotation: Optional[str] = SubjectAnnotationValidator
    professor: Optional[str] = SubjectProfessorValidator
    notes: List[Note] = SubjectNotesValidator

class SubjectOut(BaseModel):
    subject_id: Optional[int] = None
    name: str = SubjectNameValidator
    annotation: Optional[str] = SubjectAnnotationValidator
    professor: Optional[str] = SubjectProfessorValidator
    notes: List[Note] = SubjectNotesValidator

    class Config:
        orm_mode = True
