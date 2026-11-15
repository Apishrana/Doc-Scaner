from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID


class LoginModal(BaseModel):
    Email: str
    Password: str


class SignupModal(BaseModel):
    Name: str
    Email: str
    Password: str
