from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import JournalEntry, User
from app.utils.auth import decode_access_token, oauth2_scheme
from app.schemas import JournalCreate, JournalResponse
from fastapi.security import OAuth2PasswordBearer
from typing import List

router = APIRouter(
    prefix="/journal",
    tags=["journal"]
)

# 🔐 Helper to get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# 🟢 POST /journal
@router.post("/", response_model=JournalResponse)
def create_journal(
    entry: JournalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_entry = JournalEntry(
        title=entry.title,
        content=entry.content,
        user_id=current_user.id  # 👈 This links the entry to the user
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# 🔵 GET /journal
@router.get("/", response_model=List[JournalResponse])
def get_journals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Return all journal entries for current_user
    entries = db.query(JournalEntry).filter(JournalEntry.user_id == current_user.id).all()
    return entries