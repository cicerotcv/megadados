from typing import List
from uuid import uuid4


class DummyDatabase:
    def __init__(self):
        self._database: List[dict] = []

    def insert(self, subject: dict):
        if not subject.get('subject_id'):
            subject["subject_id"] = str(uuid4())
        self._database.append(subject)

    def insert_note(self, subject_id, note_value):
        subject = self.find_by_id(subject_id)
        subject_notes: list = subject["notes"]

        new_note = {
            'note_id': uuid4(),
            'value': note_value
        }

        subject_notes.append(new_note)
        self.update_by_id(subject_id, {"notes": subject_notes})
        return subject_notes

    def has(self, value, key="subject_id") -> bool:
        for subject in self._database:
            if subject[key] == value:
                return True
        return False

    def has_note(self, subject_id, note_id) -> bool:
        subject = self.find_by_id(subject_id)
        note_exists = len([note for note in subject['notes']
                          if note_id == note["note_id"]]) > 0
        return note_exists

    def delete_by_id(self, subject_id):
        self._database = [
            subject for subject in self._database if subject["subject_id"] != str(subject_id)]

    def delete_note(self, subject_id, note_id):
        subject = self.find_by_id(subject_id)
        notes = [note for note in subject["notes"]
                 if note_id != str(note['note_id'])]
        self.update_by_id(subject_id, {"notes": notes})
        return notes

    def update_note(self, subject_id, note_id, value: float):
        subject = self.find_by_id(subject_id)
        notes = subject['notes']
        for note in notes:
            if str(note['note_id']) == note_id:
                note['value'] = value
                break
        return self.update_by_id(subject_id, {"notes": notes})["notes"]

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
    "notes": [{
        "note_id": "03401e80-4d71-415f-9146-5ef734a5c22d",
        "value": 3.5
    }]
})

dummy_database.insert({
    "subject_id": "7c748cbf-5501-4e05-83d0-82866968afc0",
    "name": "Nuvem",
    "annotation": "Disciplina de redes",
    "professor": "Andrew Montagner",
    "notes": [{
        "note_id": "c89d13ca-0ca2-4d12-a4e5-099019584024",
        "value": 7.5
    }]
})

dummy_database.insert({
    "subject_id": "69c880b4-ae6c-4c85-832d-420124e50fde",
    "name": "Design de Calculadoras",
    "annotation": "Disciplina de software",
    "professor": "Igor Ayres",
    "notes": [{
        "note_id": "1e3f4915-d9a5-4777-9d43-11e21b4f296f",
        "value": 5.0
    }]
})
