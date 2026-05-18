from models import ProductFlow, Product, User
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
        query = session.query(
            ProductFlow.id,
            ProductFlow.quantity,
            ProductFlow.type,
            ProductFlow.created_at,
            Product.name.label("product_name"),
            User.name.label("user_name")
        ).join(Product, ProductFlow.product_id == Product.id)\
         .join(User, ProductFlow.user_id == User.id)
        
        if product_id is not None:
            query = query.filter(ProductFlow.product_id == product_id)

        result = query.order_by(ProductFlow.created_at.desc()).all()
        
        return [
            {
                "id": r.id,
                "product_name": r.product_name,
                "user_name": r.user_name,
                "quantity": r.quantity,
                "type": r.type,
                "created_at": r.created_at
            }
            for r in result
        ]

    except Exception as e:
        print(f"Erro no banco: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erro ao buscar o fluxo de movimentações de estoque"
        )
    