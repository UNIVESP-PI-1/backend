# 🚀 Backend FastAPI

API desenvolvida com **FastAPI**, utilizando **SQLAlchemy**, **Alembic** para migrations e **SQLite** como banco de dados.

---

## 📋 Requisitos

* Python 3.10+
* pip

---

## ⚙️ Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
cd backend
```

Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash

  cp .env.example .env # Linux / macOS
  copy .env.example .env # Windows

```

## Gere a SECRETE_KEY

Copie gere a SECRETE_KEY, copie e cole em seu .env

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🗄️ Banco de Dados

O projeto usa **SQLite** (`base.db`).

### Rodar migrations (Alembic)

```bash
alembic upgrade head
```
---

## 🌱 Populando o Banco (Seeding)

Para criar o primeiro usuário (Admin) ou cadastrar novos usuários rapidamente, utilize o script de seed. Certifique-se de que as migrations já foram executadas antes deste passo.

Ao rodar o comando, o terminal solicitará o **Nome**, **E-mail** e **Senha**.

```bash
python seed_user.py
```

Para cadastrar produtos:

```bash
python seed_product.py
```
---

## ▶️ Executando a aplicação

```bash
uvicorn main:app --reload
```

A aplicação estará disponível em:

```
http://127.0.0.1:8000
```

---

## 📚 Documentação automática

* Swagger UI:

  ```
  http://127.0.0.1:8000/docs
  ```

* Redoc:

  ```
  http://127.0.0.1:8000/redoc
  ```

---

## 📂 Estrutura do Projeto

```
.
├── alembic/          # Migrations
├── core/             # Configurações e dependências
├── routers/          # Rotas da API
├── services/         # Regras de negócio
├── models.py         # Modelos do banco
├── schemas.py        # Schemas (Pydantic)
├── main.py           # Entrada da aplicação
├── alembic.ini       # Configuração do Alembic
├── requirements.txt  # Dependências
├── seed_user.py      # Script para criar usuário inicial
```

---

## 🧪 Observações

* O banco `base.db` é local e não deve ser versionado.
* Sempre rode as migrations antes de iniciar o projeto.
* O ambiente virtual (`venv`) não deve ser versionado.

---

## 📦 Dependências principais

* FastAPI
* Uvicorn
* SQLAlchemy
* Alembic
* Pydantic
* Python-JOSE (JWT)
* Bcrypt (hash de senha)

---

## 👨‍💻 Execução rápida (resumo)

```bash
git clone <repo>
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python seed_user.py
uvicorn main:app --reload
```

---

Pronto. A API já estará rodando.
