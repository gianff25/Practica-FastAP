from utils.repositories import RepositoryBaseCRUD

from .models import UserDB


class UserRepository(RepositoryBaseCRUD):
    model = UserDB
