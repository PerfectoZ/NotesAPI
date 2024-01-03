from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["NotesApp"]
collection = db["notes"]
sequence = db["counters"]

def get_next_sequence_id(sequence_name):
    result = sequence.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True,
    )
    return result["sequence_value"]

def create_note_service(body):
    body = body.dict()
    body["_id"] = get_next_sequence_id("note_id_sequence")
    result = collection.insert_one(body)
    inserted_id = result.inserted_id
    return {"id": str(inserted_id), **body}