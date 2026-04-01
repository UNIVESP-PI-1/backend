from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryUpsertSchema(BaseModel):
    name: str


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True