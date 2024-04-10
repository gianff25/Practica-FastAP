from pydantic import ConfigDict

from utils.schemas import InclusiveModel, StrictModel


class DummyResponse(InclusiveModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
