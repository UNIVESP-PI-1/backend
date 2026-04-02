from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM= os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTS= int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTS'))
REFRESH_TOKEN_EXPIRE_MINUTS = (int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTS')))
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
