from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(String)
    image = Column(String)
    category = Column(String)
    dispatch = Column(String)
    ingredients = Column(JSON)
    portions = Column(String)