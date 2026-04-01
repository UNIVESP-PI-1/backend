from fastapi import APIRouter, Depends
from core.dependencies import get_session, get_current_user
from schemas.product_schema import ProductCreateSchema, ProductResponseSchema, ProductUpdateSchema
from services.product_service import create, get_all, get_by_id, delete, update

product_router = APIRouter(prefix='/products', tags=['products'])


@product_router.get('/')
def list_products(
    session = Depends(get_session),
    user = Depends(get_current_user)
):
    return get_all(session)


@product_router.get('/{id}')
def get_product(
    id: int,
    session = Depends(get_session),
    user = Depends(get_current_user)
):
    return get_by_id(session, id)


@product_router.post('/')
def create_product(
    schema: ProductCreateSchema,
    session = Depends(get_session),
    user = Depends(get_current_user)
):
    new_product = create(schema, session)

    return {
        "message": "Produto criado com sucesso",
        "product": ProductResponseSchema.model_validate(new_product)
    }


@product_router.delete('/{id}')
def delete_product(
    id: int,
    session = Depends(get_session),
    user = Depends(get_current_user)
):
    return delete(session, id)


@product_router.patch('/{id}')
def update_product(
    id: int,
    schema: ProductUpdateSchema,
    session = Depends(get_session),
    user = Depends(get_current_user)
):
    updated_product = update(session, id, schema)

    return {
        "message": "Produto atualizado com sucesso",
        "product": ProductResponseSchema.model_validate(updated_product)
    }