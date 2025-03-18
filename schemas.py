from pydantic import BaseModel
from typing import List

class ProductBase(BaseModel):
    name: str
    price: str
    image: str
    category: str
    dispatch: str
    ingredients: List[str]
    portions: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductsResponse(ProductBase):
    products: List[ProductResponse]