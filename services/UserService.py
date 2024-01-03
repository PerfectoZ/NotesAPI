from pymongo import MongoClient
from fastapi import HTTPException, Depends
from pymongo.errors import DuplicateKeyError
from models.User import UserCreate, UserLogin
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

class UserService:
    def __init__(self, mongo_client: MongoClient):
        self.SECRET_KEY = "secret"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.client = mongo_client
        self.db = self.client["NotesApp"]
        self.collection = self.db["users"]
        self.collection.create_index([("username", 1), ("email", 1)], unique=True)

    def create_user_service(self, body: UserCreate):
        body = body.model_dump()
        try :
            result = self.collection.insert_one(body)

        except DuplicateKeyError as e:
            raise HTTPException(status_code=400, detail="Username or Email already exists")

        body["_id"] = str(result.inserted_id)
        body.pop('password')
        return {**body}

    def create_jwt_token(self, body):
        return jwt.encode(body, key=self.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_jwt_token(self, token: str):
        try:
            payload = jwt.decode(token, key=self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        credentials_exception = HTTPException(
            status_code=401, detail="Could not validate credentials"
        )
        return self.decode_jwt_token(token)

    def login_user_service(self, body):
        body = body.model_dump()
        result = self.collection.find_one({"username":body["username"]})
        if not result:
            raise HTTPException(status_code=400, detail="Invalid Username")

        if result["password"]!=body["password"]:
            raise HTTPException(status_code=400, detail="Invalid Password")

        token_data = {"username": body["username"]}
        token = self.create_jwt_token(token_data)
        return {"access_token": token, "token_type": "bearer"}