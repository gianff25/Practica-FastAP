from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String

from utils.models import BaseModel


class TokenDB(BaseModel):
    __tablename__ = "token"
    __historical__ = True

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    token = Column(String(255), nullable=True)
