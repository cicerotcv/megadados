from typing import List, Optional
from pydantic import BaseModel
from pydantic.types import UUID


class SubjectIn(BaseModel):
    name: str
    annotation: Optional[str] = None
    professor: Optional[str] = None
    notes: List[float] = []

class SubjectOut(BaseModel):
    subject_id: Optional[UUID] = None
    name: str
    annotation: Optional[str] = None
    professor: Optional[str] = None
    notes: List[float] = []
