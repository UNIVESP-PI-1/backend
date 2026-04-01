from fastapi import APIRouter, Depends
from schemas.category_schema import CategoryUpsertSchema, CategoryResponseSchema
from core.dependencies import get_session
from core.dependencies import get_current_user
from services.category_service import create, get_all, delete, update_category

category_router = APIRouter(prefix='/category', tags=['category'])

@category_router.get('/')
def list_categories(session = Depends(get_session), user = Depends(get_current_user)):

    categories = get_all(session)
    return categories


@category_router.post('/create')
def create_category(schema: CategoryUpsertSchema, session = Depends(get_session), user = Depends(get_current_user))->dict:

    new_category = create(schema, session)

    return {
            'message': 'Categoria Criada com sucesso',
            'category': CategoryResponseSchema.model_validate(new_category)
            }


@category_router.delete('/{id}')
def delet_category(id:int, session = Depends(get_session), user = Depends(get_current_user)):
    delete_category = delete(session, id)

    return delete_category


@category_router.patch('/{id}')
def edit_category(
    id: int, 
    schema: CategoryUpsertSchema,
    session = Depends(get_session),
    user = Depends(get_current_user)
):
    updated_category = update_category(session, id, schema.name)

    return {
            'message': 'Categoria Atualizada com sucesso',
            'category': CategoryResponseSchema.model_validate(updated_category)
            }