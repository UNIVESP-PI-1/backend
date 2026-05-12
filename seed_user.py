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

def run_seed():
    print("--- Cadastro de Usuário Inicial ---")
    
    name = input("Nome do usuário: ")
    email = input("E-mail: ")
    password = input("Senha: ")

    new_user_data = UserSchema(
        name=name,
        email=email,
        password=password
    )

    try:
        new_user = auth_service.create(new_user_data, session)
        print(f"\n✅ Usuário '{new_user.name}' criado com sucesso (ID: {new_user.id})!")

    except Exception as e:
        print(f"\n❌ Erro ao adicionar usuário: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    run_seed()