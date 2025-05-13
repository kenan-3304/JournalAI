from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import db_dependency
from app.models import JournalEntry, User
from app.utils.auth import decode_access_token, oauth2_scheme
from app.schemas import JournalCreate, JournalResponse

router = APIRouter(
    prefix="/journal",
    tags=["journal"]
)

