from pydantic import BaseModel

# This file contains the Pydantic models used for request and response validation
# and serialization/deserialization in the FastAPI application.

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class JournalCreate(BaseModel):
    title: str
    content:str

class JournalResponse(JournalCreate):
    id: int
    class Config:
        orm_mode = True
        # This allows Pydantic to work with SQLAlchemy models
        # by converting them to dictionaries.

