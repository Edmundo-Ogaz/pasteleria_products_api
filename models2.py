from sqlalchemy import Table, Column, Integer, ForeignKey, String, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabla intermedia para la relación muchos a muchos
product_ingredient_association = Table(
    "products_ingredients",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("ingredient_id", ForeignKey("ingredients.id"), primary_key=True),
)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(String)
    image = Column(String)
    category = Column(String)
    dispatch = Column(String)
    ingredients = Column(JSON)
    portions = Column(String)

    ingredientList = relationship(
        "Ingredient",
        secondary=product_ingredient_association,
        back_populates="products"
    )

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    products = relationship(
        "Product",
        secondary=product_ingredient_association,
        back_populates="ingredientList"
    )