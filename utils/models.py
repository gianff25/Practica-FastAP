import uuid

from fast_alchemy_models.async_record_mixin import AsyncRecordMixin
from fast_alchemy_models.models import FastAlchemyModel
from fast_alchemy_models.simple_history import SafeDeleteMeta
from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dependencies.database import SessionLocal
from dependencies.sql_alchemy_base import Base


class CombinedMeta(SafeDeleteMeta, type(Base)):
    pass


class BaseModel(Base, AsyncRecordMixin, FastAlchemyModel, metaclass=CombinedMeta):
    __abstract__ = True
    __historical__ = False

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    created_by_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=True
    )
    updated_by_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id"), nullable=True
    )

    @declared_attr
    def created_by(cls):
        if cls.is_foreign_key(cls.created_by_id):
            return relationship(
                "UserDB", foreign_keys=[cls.created_by_id], lazy="subquery"
            )

    @declared_attr
    def updated_by(cls):
        if cls.is_foreign_key(cls.updated_by_id):
            return relationship(
                "UserDB", foreign_keys=[cls.updated_by_id], lazy="subquery"
            )

    @classmethod
    def is_foreign_key(cls, column):
        return True if column.foreign_keys else False

    @classmethod
    def get_main_class(cls):
        """
        Returns the main class of the historical model.
        """
        return BaseModel


BaseModel.set_session(SessionLocal)
