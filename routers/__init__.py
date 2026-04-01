from .auth_routes import auth_router
from .category_routes import category_router
from .product_router import product_router

routers = [
    auth_router,
    category_router,
    product_router,
]