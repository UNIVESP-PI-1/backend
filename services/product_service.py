from models import Product
from fastapi import HTTPException

def create(schema, session) -> Product:
    try:
        new_product = Product(
            name=schema.name,
            description=schema.description,
            category_id=schema.category_id,
            sku=schema.sku,
            barcode=schema.barcode,
            cost_price=schema.cost_price,
            sale_price=schema.sale_price
        )

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return new_product

    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro interno ao cadastrar produto")


def get_all(session):
    return session.query(Product).all()


def get_by_id(session, product_id: int):
    product = session.query(Product).filter(Product.id == product_id).first()

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


def update(session, product_id: int, schema):
    product = session.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if schema.name is not None:
        product.name = schema.name

    if schema.description is not None:
        product.description = schema.description

    if schema.category_id is not None:
        product.category_id = schema.category_id

    if schema.sku is not None:
        product.sku = schema.sku

    if schema.barcode is not None:
        product.barcode = schema.barcode

    if schema.cost_price is not None:
        product.cost_price = schema.cost_price

    if schema.sale_price is not None:
        product.sale_price = schema.sale_price

    try:
        session.commit()
        session.refresh(product)
        return product

    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar produto")