# coding utf-8

from fastapi import FastAPI

from . import models
from .database import engine
from .router_notes import router as notes_routes
from .router_subjects import router as subjects_routes

tags_metadata = [
    {
        "name": "subjects",
        "description": "CRUD operations involving subjects. You can **create**, **read**, **update** and **delete** subjects.",
    },
    {
        "name": "notes",
        "description": "Manage notes. These routes offer **CRUD** operations for subjects' notes.",
    },
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/")
async def root():
    return {"app": "megadados"}


app.include_router(subjects_routes)
app.include_router(notes_routes)
