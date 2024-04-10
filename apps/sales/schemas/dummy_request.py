from pydantic_async_validation import async_field_validator

from apps.placeholder.repository import DummyRepository
from utils.schemas import InclusiveModel, StrictModel


class DummyRequest(StrictModel):
    name: str
    description: str

    __repo__ = DummyRepository()

    @async_field_validator("name")
    async def validate_name(self, value):
        if (await self.__repo__.filter(name=value)).first():
            instance = self.__entity_instance__
            if instance:
                if instance.name != value:
                    raise ValueError("Name already exists")
            else:
                raise ValueError("Name already exists")
