from models import db
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException
from core.config import oauth2_scheme
from services.auth_service import validate_token

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def get_current_user(token: str = Depends(oauth2_scheme), session = Depends(get_session)):

    user = validate_token(token, session)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário inválido")
    return user