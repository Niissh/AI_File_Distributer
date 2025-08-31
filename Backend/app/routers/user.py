from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.user import UserCreate, UserOut
from app.crud import user as crud_user
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = crud_user.get_user_by_username_or_email(db, user.username)
    if existing or crud_user.get_user_by_username_or_email(db, user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    return crud_user.create_user(db, user)

@router.post("/login")
def login(username_or_email: str, password: str, db: Session = Depends(get_db)):
    u = crud_user.get_user_by_username_or_email(db, username_or_email)
    if not u or not verify_password(password, str(u.hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(u.id)})
    return {"access_token": token, "token_type": "bearer"}
