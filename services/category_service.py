from models import Category
from fastapi import HTTPException

def create(schema, session)->dict:
    try:        
        new_category = Category(schema.name)
        session.add(new_category)
        session.commit()
        session.refresh(new_category)
        
        return new_category

    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro interno ao processar o cadastro")
    
def get_all(session):
     categories = session.query(Category).all()
     return categories

def delete(session, id: int):
    category = session.query(Category).filter(Category.id == id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    try:
        session.delete(category)
        session.commit()
        return {"message": "Categoria removida com sucesso"}
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro ao deletar categoria")
    
def update_category(session, category_id: int, new_name: str):

    category = session.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    category.name = new_name
    
    try:
        session.commit()
        session.refresh(category)
        return category
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar categoria")