from pydantic import BaseModel
from typing import List

class IngredientDTO(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ProductDTO(BaseModel):
    id: int
    name: str
    price: str
    image: str
    category: str
    dispatch: str
    ingredients: List[str]
    portions: str
    ingredientList: List[IngredientDTO]

    class Config:
        orm_mode = True
