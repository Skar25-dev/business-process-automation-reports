from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
import datetime

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    category = Column(String)
    amount = Column(Float)
    customer_name = Column(String)
    date = Column(DateTime, default=datetime.timezone.utc)

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    category = Column(String)
    stock_quantity = Column(Integer) # Cantidad actual
    min_stock_level = Column(Integer) # Nivel mínimo antes de avisar
    unit_cost = Column(Float) # Lo que le cuesta a la empresa
    last_restock_date = Column(DateTime, default=datetime.timezone.utc)
