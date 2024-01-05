import os

from pymongo import MongoClient, TEXT
from fastapi import HTTPException
from models.Note import NoteCreate, NoteUpdate

class NoteService:
    def __init__(self, mongo_client: MongoClient):
        self.client = mongo_client
        self.db = self.client["NotesApp"]
        self.collection = self.db["notes"]
        self.sequence = self.db["counters"]
        self.sharing = self.db["shared_notes"]
        try: self.collection.create_index([("title", TEXT), ("body", TEXT)])
        except: pass

    def get_note_id(self, sequence_name):
        result = self.sequence.find_one_and_update(
            {"_id": sequence_name},
            {"$inc": {"sequence_value": 1}},
            upsert=True,
            return_document=True,
        )
        return result["sequence_value"]

    def create_note_service(self, body:NoteCreate, user):
        body = body.model_dump()
        print(user)
        body["created_by"] = user["username"]
        body["_id"] = self.get_note_id("note_id_sequence")
        result = self.collection.insert_one(body)
        inserted_id = result.inserted_id
        return {"id": inserted_id, **body}

    def get_note_service(self, id, user):
        document = self.collection.find_one({"_id": id})
        if document is None:
            raise HTTPException(status_code=404, detail=f'No Note Found with id: {id}')
        if document["created_by"]!=user["username"]:
            raise HTTPException(status_code=403, detail="Cannot view someone else's Note")
        return document

    def get_all_notes_service(self, username):
        return list(self.collection.find({"created_by": username}))

    def update_note_service(self, id, body:NoteUpdate, user):
        document = self.get_note_service(id, user)
        body = body.model_dump()
        for k in body.keys():
            if body[k]:
                document[k] = body[k]
        self.collection.update_one({"_id": id}, {"$set": document})
        document.pop("_id")
        return document

    def delete_note_service(self, id, user):
        document = self.get_note_service(id, user)
        if document["created_by"]!=user["username"]:
            raise HTTPException(detail="Cannot delete other's Note", status_code=403)
        self.collection.delete_one({"_id": id})
        return {"message": "Deleted Successfully"}

    def share_note_service(self, id, body, user):
        self.get_note_service(id, user)
        body = body.model_dump()
        body["fromUser"] = user["username"]
        body["noteId"] = id
        self.sharing.insert_one(body)
        body["_id"] = str(body["_id"])
        return body

    def search_keywords_service(self, query):
        return list(self.collection.find(
            {
                "$text": {
                    "$search": query
                }
            },
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]))