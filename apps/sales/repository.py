from utils.repositories import RepositoryBaseCRUD

from .models import DummyDB


class DummyRepository(RepositoryBaseCRUD):
    model = DummyDB
