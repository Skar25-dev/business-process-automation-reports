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
