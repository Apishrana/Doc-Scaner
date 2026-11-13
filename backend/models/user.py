from uuid import UUID

from pydantic import AwareDatetime, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID


class User(BaseModel):
    Id: UUID
    User_name: str
    Email: str
    Role: str


class UserDB(User):
    Password_hash: str
    Fcm_token: str | None = None
    Created_at: AwareDatetime

class LoginModal(BaseModel):
    Email:str
    Password:str

class SignupModal(BaseModel):
    Name:str
    Email:str
    Password:str