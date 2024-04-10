from copy import copy
from datetime import datetime

from utils.models import BaseModel


class RepositoryBaseCRUD:
    """
    Base class For repositories
    """

    model: BaseModel

    def __init__(self, current_user=None):
        self.current_user = current_user

    async def get_all(self, **kwargs):
        return (await self.model.where_async(**kwargs)).all()

    async def filter(self, **kwargs):
        return await self.model.where_async(**kwargs)

    async def create(self, **kwargs):
        if self.current_user:
            kwargs["created_by_id"] = self.current_user.id
        return await self.model.create_async(**kwargs)

    async def update(self, changes, item):
        changes = (
            changes.dict(exclude_unset=True) if hasattr(changes, "dict") else changes
        )
        if self.current_user:
            changes["updated_by_id"] = self.current_user.id
        await item.update_async(**changes, updated_at=datetime.utcnow())
        return item

    async def upsert(self, defaults: dict = {}, **criteria):
        result = (await self.filter(**criteria)).first()
        fields = copy(defaults)

        if result:
            return await self.update(fields, result)
        else:
            fields.update(criteria)
            return await self.create(**fields)

    async def get_or_create(self, defaults: dict = {}, **criteria):
        result = (await self.filter(**criteria)).first()
        fields = copy(defaults)
        fields.update(criteria)

        if result:
            return result
        else:
            return await self.create(**fields)

    async def find_or_fail(self, id: int):
        item = (await self.model.where_async(id=id, deleted=None)).first()
        if not item:
            raise Exception(f"{self.model.__name__} not found")
        return item

    async def delete(self, item):
        item = await item.update_async(deleted=datetime.utcnow())
        return item
