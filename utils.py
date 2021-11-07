from typing import List
from uuid import uuid4


class DummyDatabase:
    def __init__(self):
        self._database: List[dict] = []

    def insert(self, subject: dict):
        if not subject.get('subject_id'):
            subject["subject_id"] = str(uuid4())
        self._database.append(subject)

    def has(self, value, key="subject_id") -> bool:
        for subject in self._database:
            if subject[key] == value:
                return True
        return False

    def delete_by_id(self, subject_id):
        self._database = [
            subject for subject in self._database if subject["subject_id"] != str(subject_id)]

    def find_by_id(self, subject_id):
        for subject in self._database:
            if subject["subject_id"] == str(subject_id):
                return {**subject}

    def list(self):
        return [{**item} for item in [*self._database]]

    def update_by_id(self, subject_id, data: dict):
        for index, subject in enumerate(self._database):
            if subject["subject_id"] == str(subject_id):
                for key, value in data.items():
                    if value != None:
                        subject[key] = value
                self._database[index] = subject
                return {**subject}


dummy_database = DummyDatabase()
dummy_database.insert({
    "subject_id": "08c4ff5e-a854-4a4b-833a-211dd77fc6da",
    "name": "Microdados",
    "annotation": "Disciplina de banco de dados",
    "professor": "Fabio Toshimoto",
    "notes": []
})

dummy_database.insert({
    "subject_id": "7c748cbf-5501-4e05-83d0-82866968afc0",
    "name": "Nuvem",
    "annotation": "Disciplina de redes",
    "professor": "Andrew Montagner",
    "notes": []
})

dummy_database.insert({
    "subject_id": "69c880b4-ae6c-4c85-832d-420124e50fde",
    "name": "Design de Calculadoras",
    "annotation": "Disciplina de software",
    "professor": "Igor Ayres",
    "notes": []
})
