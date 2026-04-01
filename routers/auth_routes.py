from fastapi import APIRouter, Depends, Header
from core.dependencies import get_session, get_current_user
from services.auth_service import create, auth_user, gen_token, validate_token
from models import User
from schemas.auth_schema import UserCreateSchema, UserResponseSchema, LoginSchema

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
def list_users(user: User = Depends(get_current_user))->dict:
    return {'users': user}


@auth_router.post('/create_acount')
def create_acount(schema: UserCreateSchema, session = Depends(get_session)):
    new_user = create(schema, session)

    return {
        "message": "Usuário criado com sucesso",
        "product": UserResponseSchema.model_validate(new_user)
    }
    

@auth_router.post('/login')
def login(schema: LoginSchema, session = Depends(get_session)):
    
    return auth_user(schema, session)
    

@auth_router.get('/refresh')
def refresh_token(
    authorization: str = Header(...),
    session = Depends(get_session)
):
    token = authorization.replace("Bearer ", "")
    
    user = validate_token(token, session, 'refresh')
    access_token = gen_token(user.id)

    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }
    
