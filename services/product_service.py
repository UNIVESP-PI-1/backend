from models import Product
from fastapi import HTTPException
from services import product_flow_service

def create(schema, session, user_id) -> Product:
    try:
        new_product = Product(
            name=schema.name,
            description=schema.description,
            category_id=schema.category_id,
            sku=schema.sku,
            barcode=schema.barcode,
            cost_price=schema.cost_price,
            sale_price=schema.sale_price,
            stock_quantity=schema.stock_quantity,
            min_stock=schema.min_stock,
            status=schema.status,
        )

        session.add(new_product)
        session.flush() 

        if new_product.stock_quantity > 0:
            product_flow_service.log_movement(
                session=session,
                product_id=new_product.id,
                user_id=user_id,
                quantity=new_product.stock_quantity,
                flow_type="ENTRADA",
            )

        session.commit()
        session.refresh(new_product)
        return new_product

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro interno ao cadastrar produto")


def get_all(session):
    return session.query(Product).all()


def get_by_id(session, product_id: int):
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


def get_by_barcode(session, product_barcode: str):
    product = session.query(Product).filter(Product.barcode == product_barcode).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


def delete(session, product_id: int):
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    try:
        session.delete(product)
        session.commit()
        return {"message": "Produto removido com sucesso"}

    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro ao deletar produto")


def update(session, product_id: int, schema, user_id):
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if schema.name is not None: product.name = schema.name
    if schema.description is not None: product.description = schema.description
    if schema.category_id is not None: product.category_id = schema.category_id
    if schema.sku is not None: product.sku = schema.sku
    if schema.barcode is not None: product.barcode = schema.barcode
    if schema.cost_price is not None: product.cost_price = schema.cost_price
    if schema.sale_price is not None: product.sale_price = schema.sale_price
    if schema.min_stock is not None: product.min_stock = schema.min_stock
    if schema.status is not None: product.status = schema.status

    # LÓGICA DE MOVIMENTAÇÃO DE ESTOQUE
    if schema.stock_quantity is not None:
        # Pega a quantidade antiga que estava salva no banco antes de alterar
        old_stock = product.stock_quantity
        new_stock = schema.stock_quantity
        
        if old_stock != new_stock:
            # Calcula a variação matemática
            diff = new_stock - old_stock
            flow_type = "ENTRADA" if diff > 0 else "SAIDA"

            product.stock_quantity = new_stock

            product_flow_service.log_movement(
                session=session,
                product_id=product.id,
                user_id=user_id,
                quantity=abs(diff),
                flow_type=flow_type,
            )

    try:
        session.commit()
        session.refresh(product)
        return product

    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar produto")