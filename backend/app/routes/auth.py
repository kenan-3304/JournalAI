from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import db_dependency
from app.schemas import UserCreate, UserLogin, Token
from app.models import User
from app.utils import auth as auth_utils  # for hashing, token creation

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# 🟩 Register Route
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: db_dependency):
    if (db.query(User).filter(User.username == user.username).first()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    my_user = User(
        username=user.username,
        email=user.email,
        hashed_password=auth_utils.get_password_hash(user.password)
    )

    db.add(my_user)
    db.commit()
    db.refresh(my_user)


    return {
        "access_token": auth_utils.create_access_token(data={"sub": user.username}),
        "token_type": "bearer"
    }
    # 1. Check if username already exists in DB
    # 2. Hash password
    # 3. Create User object
    # 4. Add to DB
    # 5. Return JWT token using auth_utils.create_access_token()


# 🟦 Login Route
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: db_dependency):

    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not auth_utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {
        "access_token": auth_utils.create_access_token(data={"sub": user.username}),
        "token_type": "bearer"
    }
    # 1. Get user from DB by username
    # 2. If user not found, raise 401
    # 3. Verify password using auth_utils.verify_password()
    # 4. If invalid, raise 401
    # 5. Create JWT token and return
