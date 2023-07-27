from pydantic import BaseModel

class User(BaseModel):
    token: str
    uid: str
    displayName: str
    email: str
    photoURL: str