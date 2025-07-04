from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from src.auth_utility import AuthUtility
from src.db.database import get_db
from src.db.models import User
from src.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(400, "Username already registered")
    hashed_password = AuthUtility.hash_password(user_in.password)
    user = User(username=user_in.username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not AuthUtility.verify_password(password, user.hashed_password):
        raise HTTPException(400, "Incorrect username or password")
    access_token = AuthUtility.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
