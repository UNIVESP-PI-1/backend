from pydantic import BaseModel
from typing import Optional

class ProductCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    sku: str
    barcode: Optional[str] = None
    cost_price: int
    sale_price: int
    stock_quantity = int
    min_stock = int
    status = bool

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    cost_price: Optional[int] = None
    sale_price: Optional[int] = None
    stock_quantity = Optional[int] = None
    min_stock = Optional[int] = None
    status = Optional[bool] = None

class ProductResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category_id: int
    sku: str
    barcode: Optional[str]
    cost_price: int
    sale_price: int
    stock_quantity = int
    min_stock = int
    status = bool

    class Config:
        from_attributes = True