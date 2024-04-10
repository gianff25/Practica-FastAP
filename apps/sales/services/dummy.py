from apps.placeholder.models import DummyDB
from apps.placeholder.repository import DummyRepository
from apps.placeholder.schemas.dummy_response import DummyResponse
from utils.schemas import MessageResponse
from utils.services import BaseService


class DummyService(BaseService):
    def __init__(self, current_user=None):
        super().__init__(current_user=current_user)
        self.repo = DummyRepository(current_user=current_user)

    def test(self):
        return MessageResponse(message="Hello")
