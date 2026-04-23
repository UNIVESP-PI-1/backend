from models import User
from fastapi import HTTPException
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES

def create(schema, session):
    user = session.query(User).filter(User.email == schema.email).first()

    if user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    
    try:
        pwd_bytes = schema.password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
        
        new_user = User(schema.name, schema.email, password_hash)
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        return new_user

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro interno ao processar o cadastro")

def auth_user(schema, session):
    user = session.query(User).filter(User.email==schema.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    
    password_match = bcrypt.checkpw(
        schema.password.encode('utf-8'), 
        user.password.encode('utf-8')
    )

    if not password_match:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos") 
    
    access_token = gen_token(user.id)
    reflesh_token = gen_token(user.id, 'refresh', REFRESH_TOKEN_EXPIRE_MINUTES)
    return {
        'message': 'Usuario logado',
        'token': access_token,
        'reflesh_token': reflesh_token,
        'token_type': 'Bearer'
        }
    
def gen_token(user_id, token_type = 'access', expire_token=ACCESS_TOKEN_EXPIRE_MINUTES):
    expire_date = datetime.now(timezone.utc) + timedelta(minutes=expire_token)
    
    expire_timestamp = int(expire_date.timestamp())
    
    info = {
        'sub': str(user_id),
        'exp': expire_timestamp,
        'type': token_type 
    }
    
    token_jwt = jwt.encode(info, SECRET_KEY, algorithm=ALGORITHM)

    return token_jwt


def validate_token(token, session, expected_type="access"):
    payload = _decode_token(token)
    
    if payload.get("type") != expected_type:
            raise HTTPException(status_code=401, detail="Token de acesso inválido")
        
    user_id = payload.get('sub')
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return user

def _decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")