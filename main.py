from fastapi import FastAPI

app = FastAPI()

from routers.auth_routes import auth_router
from routers.category_routes import category_router

app.include_router(auth_router)
app.include_router(category_router)
