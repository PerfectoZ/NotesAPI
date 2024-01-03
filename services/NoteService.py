from pymongo import MongoClient
from fastapi import HTTPException

client = MongoClient("mongodb://localhost:27017/")
db = client["NotesApp"]
collection = db["notes"]
sequence = db["counters"]

def get_note_id(sequence_name):
    result = sequence.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True,
    )
    return result["sequence_value"]

def create_note_service(body):
    body = body.model_dump()
    body["_id"] = get_note_id("note_id_sequence")
    result = collection.insert_one(body)
    inserted_id = result.inserted_id
    return {"id": inserted_id, **body}

def get_note_service(id):
    document = collection.find_one({"_id": id})
    if document is None:
        raise HTTPException(status_code=404, detail=f'No Note Found with id: {id}')
    return document

def get_all_notes_service():
    return list(collection.find())

def update_note_service(id, body):
    document = get_note_service(id)
    body = body.model_dump()
    for k in body.keys():
        if body[k]:
            document[k] = body[k]
    collection.update_one({"_id": id}, {"$set": document})
    document.pop("_id")
    return document



