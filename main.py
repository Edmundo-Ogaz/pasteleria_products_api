from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas
import database
from typing import List

app = FastAPI()

# Crear tablas
models.Base.metadata.create_all(bind=database.engine)

# Dependencia de la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=schemas.ProductResponse)
def crear_usuario(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(name=product.name, price=product.price, image=product.image, category=product.category, dispatch=product.dispatch, ingredients=product.ingredients, portions=product.portions)
    # db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def obtener_usuario(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/ingredients/{ingredient}", response_model=List[schemas.ProductResponse])
def obtener_usuario(ingredient: str, db: Session = Depends(get_db)):
    # product = db.query(models.Product).filter(models.Product.id == product_id).first()
    # products = db.query(models.Product).filter(func.json_extract(models.Product.ingredients, '$[*]') == ingredient).all()
    # products = db.query(models.Product).filter(models.Product.ingredients.like(ingredient)).all()

    search_term = ingredient.upper()

    all_products = db.query(models.Product).all()
    
    # Filtramos manualmente los productos que contienen el ingrediente
    filtered_products = []
    for product in all_products:
        # Convertir la cadena JSON a lista
        ingredients_list = product.ingredients

        # Convertir cada ingrediente a mayúsculas y verificar si contiene el término de búsqueda
        # if any(search_term in ing.upper() for ing in ingredients_list):
        #     filtered_products.append(product)

        for element in ingredients_list:
            if search_term in element:
                filtered_products.append(product)

    return filtered_products
