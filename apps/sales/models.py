# You can define your models here
# Here is an example

from sqlalchemy import Column, Integer, Float, JSON

from utils.models import BaseModel


class SalesDB(BaseModel):
    __tablename__ = "sales"
    __historical__ = True

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float)
    products = Column(JSON)
