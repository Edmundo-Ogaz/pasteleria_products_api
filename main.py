from fastapi import FastAPI, Depends, Query,  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func

from database_postgres import get_db, engine, Base
from models2 import Product, Ingredient, product_ingredient_association
from schemas2 import ProductDTO
from utils import singular
from typing import List, Optional

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicio (startup)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas")
    except Exception as e:
        print("❌ Error al crear tablas:", e)

    yield  # Aquí arranca la app FastAPI

    # Código de cierre (shutdown) — opcional
    # await engine.dispose()
    print("🛑 Aplicación cerrada")

app = FastAPI(lifespan=lifespan)

# app = FastAPI()

# # Crear tablas al inicio
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@app.get("/api/v2.0/products/{id}", response_model=ProductDTO)
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

@app.get("/products/test")
async def leer_usuarios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    usuarios = result.scalars().all()
    return usuarios

@app.get("/api/v1.0/products", response_model=List[ProductDTO])
async def get_products(
    ingredients: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    if ingredients:
        print("get_products by ingredients", ingredients)
        return await searchIngredients2(db, ingredients, "ALL")
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.ingredientList))
    )
    print("get_products")
    return result.scalars().all()

@app.get("/api/v1.0/products/cakes", response_model=List[ProductDTO])
async def get_cakes_by_ingredients(
    ingredients: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    print("get_cakes_by_ingredients", ingredients)
    response = await searchIngredients2(db, ingredients, "Tortas")

    print("get_cakes_by_ingredients response", len(response))
    return response

@app.get("/api/v1.0/products/desserts", response_model=List[ProductDTO])
async def get_desserts_by_ingredients(
    ingredients: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    print("get_desserts_by_ingredients", ingredients)
    response = await searchIngredients2(db, ingredients, "Postres")

    print("get_desserts_by_ingredients response", len(response))
    return response

@app.get("/api/v1.0/products/cocktails", response_model=List[ProductDTO])
async def get_cocktails_by_ingredients(
    ingredients: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    print("get_cocktails_by_ingredients", ingredients)
    response = await searchIngredients2(db, ingredients, "Cocktel")

    print("get_cocktails_by_ingredients response", len(response))
    return response

@app.get("/api/v1.0/products/kutchens", response_model=List[ProductDTO])
async def get_kutchens_by_ingredients(
    ingredients: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    print("get_kutchens_by_ingredients", ingredients)
    response = await searchIngredients2(db, ingredients, "Kutchen")

    print("get_kutchens_by_ingredients response", len(response))
    return response

async def searchIngredients2( db: AsyncSession, ingredients: str, category: str):
    print("searchIngredients2", ingredients, category)
    response = []

    if not ingredients.strip():
        return response

    array_ingredients = ingredients.strip().split(",")
    ingredient_names = [singular(e).lower() for e in array_ingredients]
    print("searchIngredients2", ingredient_names)

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
    print("searchIngredients2 size", len(db_products))

    for product in db_products:
        if "ALL" == category or product.category == category:
            response.append(product)

    print("searchIngredients2 response", len(response))
    return response
