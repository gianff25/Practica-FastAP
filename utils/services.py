from typing import Any

from fastapi import HTTPException, status

from apps.placeholder.exceptions import PlaceholderException
from dependencies.context.exception import ExceptionContext
from dependencies.context.request import RequestContext
from dependencies.context.user import UserContext
from utils.fastapi import ensure_request_validation_errors
from utils.repositories import RepositoryBaseCRUD


class BaseService(UserContext, RequestContext, ExceptionContext):
    """
    Base service class providing common CRUD operations.

    Attributes:
        __response__ (callable): A callable used for generating responses.
        __model__ (BaseModel): The model associated with the service.
    """

    __response__ = None
    repo: RepositoryBaseCRUD

    def __init__(self, current_user=None):
        self.current_user = current_user

    async def create(self, item):
        """
        Create a new item.

        args:
            item (Any): The item to be created.

        returns:
            BaseModel: The created item.

        raises:
            BaseException: If an exception occurs during creation.
        """
        # tactica, catalogica & normativa validations
        with ensure_request_validation_errors():
            # validate async_field_validator & async_model_validator
            await item.model_async_validate()
        return await self.repo.create(**item.dict())

    async def delete(self, id: int):
        """
        Delete an item.

        args:
            id (int): The ID of the item to be deleted.

        returns:
            BaseModel: The deleted item.

        raises:
            BaseException: If an exception occurs during deletion.
        """
        item = (await self.repo.filter(id=id)).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return await self.repo.delete(item)

    async def get(self, id):
        """
        Get an item by ID.

        args:
            id (int): The ID of the item to retrieve.

        returns:
            BaseModel: The retrieved item.

        raises:
            BaseException: If the item does not exist.
        """
        return await self.repo.find_or_fail(id=id)

    async def update(self, id, changes):
        """
        Update an item.

        args:
            id (int): The ID of the item to be updated.
            changes (Any): The changes to be applied to the item.

        returns:
            BaseModel: The updated item.

        raises:
            BaseException: If an exception occurs during update.
        """
        item = (await self.repo.filter(id=id)).first()
        # tactica, catalogica & normativa validations
        with ensure_request_validation_errors():
            # validate async_field_validator & async_model_validator
            await changes.model_async_validate(item)
        return await self.repo.update(changes, item)

    async def get_all(self, **query):
        """
        Get all items.

        returns:
            list[Any]: A list of all items.

        raises:
            BaseException: If an exception occurs while retrieving all items.
        """
        return await self.repo.get_all(**query)

    async def upsert(self, defaults: dict = {}, **criteria):
        """
        Upsert (update or insert) an item.

        args:
            id (int): The ID of the item to be upserted.
            changes (Any): The changes to be applied to the item.

        returns:
            BaseModel: The upserted item.

        raises:
            BaseException: If an exception occurs during upsert.
        """
        return await self.repo.upsert(defaults=defaults, **criteria)

    async def get_or_create(self, defaults: dict = {}, **criteria):
        """
        Get an item by ID or create it if it does not exist.

        args:
            id (int): The ID of the item to retrieve or create.
            item (Any): The item to create if it does not exist.

        returns:
            BaseModel: The retrieved or created item.

        raises:
            BaseException: If an exception occurs during retrieval or creation.
        """
        return await self.repo.get_or_create(defaults=defaults, **criteria)
