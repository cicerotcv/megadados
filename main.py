# coding utf-8

from router_notes import router as notes_routes
from router_subjects import router as subjects_routes
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "subjects",
        "description": "CRUD operations involving subjects. You can **create**, **read**, **update** and **delete** subjects."
    },
    {
        "name": "notes",
        "description": "Manage notes. These routes offer **CRUD** operations for subjects' notes."
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/")
async def root():
    return {"app": "megadados"}


app.include_router(subjects_routes)
app.include_router(notes_routes)
