from pymongo import MongoClient
from fastapi import HTTPException, Depends
from pymongo.errors import DuplicateKeyError
from models.User import UserCreate, UserLogin
from fastapi.security import OAuth2PasswordBearer
import bcrypt
import paseto
from paseto.keys.symmetric_key import SymmetricKey
from paseto.protocols.v4 import ProtocolVersion4

SECRET_KEY = SymmetricKey.generate(protocol=ProtocolVersion4)

class UserService:
    def __init__(self, mongo_client: MongoClient):
        self.SECRET_KEY = SECRET_KEY
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.client = mongo_client
        self.db = self.client["NotesApp"]
        self.collection = self.db["users"]
        self.collection.create_index([("username", 1), ("email", 1)], unique=True)

    def create_user_service(self, body: UserCreate):
        body = body.model_dump()
        hashed_password = bcrypt.hashpw(body["password"].encode("utf-8"), bcrypt.gensalt())
        body["password"] = hashed_password.decode("utf-8")

        try :
            result = self.collection.insert_one(body)

        except DuplicateKeyError as e:
            raise HTTPException(status_code=400, detail="Username or Email already exists")

        body["_id"] = str(result.inserted_id)
        body.pop('password')
        return {**body}

    def create_paseto_token(self, body):
        token = paseto.create(key=self.SECRET_KEY,
                              purpose='local',
                              claims={"username": body["username"]},
                              exp_seconds=300)
        return token

    def decode_paseto_token(self, token: str):
        try:
            claims = paseto.parse(
                key=self.SECRET_KEY,
                purpose='local',
                token=token,
            )
            return claims['message']
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
          
    def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        credentials_exception = HTTPException(
            status_code=401, detail="Could not validate credentials"
        )
        return self.decode_paseto_token(token)

    def login_user_service(self, body):
        body = body.model_dump()
        result = self.collection.find_one({"username":body["username"]})
        if not result:
            raise HTTPException(status_code=400, detail="Invalid Username")

        stored_password = result["password"].encode("utf-8")

        if not bcrypt.checkpw(body["password"].encode("utf-8"), stored_password):
            raise HTTPException(status_code=400, detail="Invalid Password")

        token_data = {"username": body["username"]}
        token = self.create_paseto_token(token_data)
        return {"access_token": token}

    def get_user_by_username(self, username):
        result = self.collection.find_one({"username": username})
        if not result :
            raise HTTPException(status_code=404, detail="No User found")
        return True