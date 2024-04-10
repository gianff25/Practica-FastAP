from typing import Optional

from utils.schemas import InclusiveModel, StrictModel


class DummyFilter(StrictModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
