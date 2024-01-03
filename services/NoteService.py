from pymongo import MongoClient
from fastapi import HTTPException
from models.Note import NoteCreate, NoteUpdate

class NoteService:
    def __init__(self, mongo_client: MongoClient):
        self.client = mongo_client
        self.db = self.client["NotesApp"]
        self.collection = self.db["notes"]
        self.sequence = self.db["counters"]

    def get_note_id(self, sequence_name):
        result = self.sequence.find_one_and_update(
            {"_id": sequence_name},
            {"$inc": {"sequence_value": 1}},
            upsert=True,
            return_document=True,
        )
        return result["sequence_value"]

    def create_note_service(self, body: NoteCreate):
        body = body.model_dump()
        body["_id"] = self.get_note_id("note_id_sequence")
        result = self.collection.insert_one(body)
        inserted_id = result.inserted_id
        return {"id": inserted_id, **body}

    def get_note_service(self, id):
        document = self.collection.find_one({"_id": id})
        if document is None:
            raise HTTPException(status_code=404, detail=f'No Note Found with id: {id}')
        return document

    def get_all_notes_service(self):
        return list(self.collection.find())

    def update_note_service(self, id, body:NoteUpdate):
        document = self.get_note_service(id)
        body = body.model_dump()
        for k in body.keys():
            if body[k]:
                document[k] = body[k]
        self.collection.update_one({"_id": id}, {"$set": document})
        document.pop("_id")
        return document

    def delete_note_service(self, id):
        self.collection.delete_one({"_id": id})
        return {"message": "Deleted Successfully"}
