from models import ProductFlow
from fastapi import HTTPException

def log_movement(session, product_id: int, user_id: int, quantity: int, flow_type: str = None):
    
    if quantity == 0:
        return

    new_flow = ProductFlow(
        product_id=product_id,
        user_id=user_id,
        quantity=abs(quantity),
        type=flow_type,
    )
    
    session.add(new_flow)

def get_flow(session, product_id: int = None):
    try:
        query = session.query(ProductFlow)
        
        if product_id is not None:
            query = query.filter(ProductFlow.product_id == product_id)

        return query.order_by(ProductFlow.created_at.desc()).all()

    except Exception:
        raise HTTPException(
            status_code=500, 
            detail="Erro ao buscar o fluxo de movimentações de estoque"
        )