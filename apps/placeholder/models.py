# You can define your models here
# Here is an example

from sqlalchemy import Column, Integer, String

from utils.models import BaseModel


class DummyDB(BaseModel):
    __tablename__ = "dummy"
    __historical__ = True

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(16))
    description = Column(String(64))
