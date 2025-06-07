
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from typing import List, Optional

from database_postgres_serverless import SessionLocal
from models2 import Product, Ingredient, product_ingredient_association
from schemas2 import ProductDTO
from utils import singular

app = FastAPI()

# Inyectar sesión por request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/products/{id}", response_model=ProductDTO)
def get_product(id: int, db: Session = Depends(get_db)):
    print(f"getProduct {id}")
    product = db.execute(
        select(Product)
        .options(selectinload(Product.ingredientList))
        .where(Product.id == id)
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.scalar_one_or_none()

@app.get("/api/v1.0/products", response_model=List[ProductDTO])
def get_products(
    ingredients: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    if ingredients:
        print("get_products by ingredients", ingredients)
        return searchIngredients2(db, ingredients, "ALL")
    result = db.execute(
        select(Product)
        .options(selectinload(Product.ingredientList))
    )
    print("get_products")
    return result.scalars().all()

@app.get("/api/v1.0/products/cakes", response_model=List[ProductDTO])
def get_cakes_by_ingredients(
    ingredients: str = Query(...),
    db: Session = Depends(get_db)
):
    print("get_cakes_by_ingredients", ingredients)
    response = searchIngredients2(db, ingredients, "Tortas")

    print("get_cakes_by_ingredients response", len(response))
    return response

@app.get("/api/v1.0/products/desserts", response_model=List[ProductDTO])
def get_desserts_by_ingredients(
    ingredients: str = Query(...),
    db: Session = Depends(get_db)
):
    print("get_desserts_by_ingredients", ingredients)
    response = searchIngredients2(db, ingredients, "Postres")

    print("get_desserts_by_ingredients response", len(response))
    return response

@app.get("/api/v1.0/products/cocktails", response_model=List[ProductDTO])
def get_cocktails_by_ingredients(
    ingredients: str = Query(...),
    db: Session = Depends(get_db)
):
    print("get_cocktails_by_ingredients", ingredients)
    response = searchIngredients2(db, ingredients, "Cocktel")

    print("get_cocktails_by_ingredients response", len(response))
    return response

@app.get("/api/v1.0/products/kutchens", response_model=List[ProductDTO])
def get_kutchens_by_ingredients(
    ingredients: str = Query(...),
    db: Session = Depends(get_db)
):
    print("get_kutchens_by_ingredients", ingredients)
    response = searchIngredients2(db, ingredients, "Kutchen")

    print("get_kutchens_by_ingredients response", len(response))
    return response

def searchIngredients2( db: Session, ingredients: str, category: str):
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
    result = db.execute(stmt)
    db_products = result.scalars().all()
    print("searchIngredients2 size", len(db_products))

    for product in db_products:
        if "ALL" == category or product.category == category:
            response.append(product)

    print("searchIngredients2 response", len(response))
    return response



