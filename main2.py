from fastapi import FastAPI, Depends, Query,  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func

from database_postgres import get_db, engine, Base
from models2 import Product, Ingredient, product_ingredient_association
from schemas2 import ProductDTO
from utils import singularizar
from typing import List

app = FastAPI()

# Crear tablas al inicio
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/products/")
async def leer_usuarios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    usuarios = result.scalars().all()
    return usuarios

@app.get("/api/v1.0/products/{id}", response_model=ProductDTO)
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    print(f"getProduct {id}")
    product = await db.execute(
        select(Product)
        .options(selectinload(Product.ingredientList))
        .where(Product.id == id)
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.scalar_one_or_none()

@app.get("/kutchens", response_model=List[ProductDTO])
async def get_kutchens_by_ingredients(
    ingredients: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    print("getKutchensByIngredients", ingredients)
    response = []

    if not ingredients.strip():
        return response

    array_ingredients = ingredients.strip().split(",")
    ingredient_names = [singularizar(e).lower() for e in array_ingredients]
    print("getProducts", ingredient_names)

    stmt = (
        select(Product)
        .join(product_ingredient_association)
        .join(Ingredient)
        .where(func.lower(Ingredient.name).in_(ingredient_names))
        .group_by(Product.id)
        .having(func.count(func.distinct(Ingredient.id)) == len(ingredient_names))
        .options(selectinload(Product.ingredientList))
    )
    result = await db.execute(stmt)
    db_products = result.scalars().all()
    print("getProducts size", len(db_products))

    for product in db_products:
        if product.category == "Kutchen":  # O usa .lower() si necesitas comparar insensible a mayúsculas
            response.append(product)

    print("getKutchensByIngredients response", len(response))
    return response
