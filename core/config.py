from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM= os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_MINUTES = (int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')))
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
