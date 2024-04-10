from utils.repositories import RepositoryBaseCRUD

from .models import TokenDB


class AuthRepository(RepositoryBaseCRUD):
    model = TokenDB
