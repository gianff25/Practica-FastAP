from typing import Any, List, Optional, Type

from pydantic import BaseModel
from pydantic_async_validation import AsyncValidationModelMixin


class BaseSchema(BaseModel):
    """
    Base class for all schemas.
    """

    def get_query(self):
        params_dict = self.dict()
        query = {}
        for key, value in params_dict.items():
            if value:
                new_key = key.replace("filter_by_", "")
                query[new_key] = value

            if value == False:
                new_key = key.replace("filter_by_", "")
                query[new_key] = value

        return query

    @classmethod
    async def transformer(cls, obj_list) -> List["BaseModel"]:
        return [await cls.model_validate(obj) for obj in obj_list]

    @classmethod
    async def model_validate(cls: Type[BaseModel], obj: Any) -> BaseModel:
        return super().model_validate(obj)  # type: ignore


class StrictModel(AsyncValidationModelMixin, BaseSchema):
    """
    Ensures Schema has no extra fields.
    """

    class Config:
        extra = "forbid"

    async def model_async_validate(self, instance=None) -> None:
        self.__entity_instance__ = instance
        await super().model_async_validate()


class InclusiveModel(BaseSchema):
    """
    Includes None values in the resulting dictionary.
    """

    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_none"] = False  # "True" excludes None values.
            return BaseModel.dict(self, *args, **kwargs)


class MessageResponse(InclusiveModel):
    """
    Response schema for messages
    """

    message: Optional[str]
