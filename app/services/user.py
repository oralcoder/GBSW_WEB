from models.user import User  # SQLAlchemy 모델
from sqlalchemy.orm import Session
from schemas.user import UserRegister, UserLogin
from core.security import hash_password, verify_password
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


async def register_user(db: Session, user_data: UserRegister):
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        userid=user_data.userid,
        password=hashed_password,
        name=user_data.name,
        email=user_data.email,
        created_at=datetime.utcnow()
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User ID or Email already exists")

async def authenticate_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.userid == login_data.userid).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid userID or password")

    return user