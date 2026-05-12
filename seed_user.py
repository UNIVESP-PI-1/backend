from models import db, User
from sqlalchemy.orm import sessionmaker
from services import auth_service

Session = sessionmaker(bind=db)
session = Session()

class UserSchema:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

new_user_data = UserSchema(
    name="Novo Usuário",
    email="novo@email.com",
    password="sua_senha_segura"
)

try:
    new_user = auth_service.create(new_user_data, session)
    
    print(f"Usuário '{new_user.name}' criado com sucesso com ID: {new_user.id}!")

except Exception as e:
    print(f"Erro ao adicionar usuário: {e}")

finally:
    session.close()