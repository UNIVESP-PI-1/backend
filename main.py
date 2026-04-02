from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import routers
from core.config import FRONTEND_URL

app = FastAPI()

# Configura as permissões de acesso
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)